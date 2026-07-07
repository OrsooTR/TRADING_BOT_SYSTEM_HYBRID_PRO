from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

import backtrader as bt
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from derivatives_bt.backtest import RunConfig, TradeStatsAnalyzer
from derivatives_bt.data_utils import load_histdata_zips, resample_ohlcv, split_frame


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "fft_clock_filter_backtests"
DATA_ROOT = ARTIFACT_ROOT / "data"
REPORT_ROOT = ARTIFACT_ROOT / "reports"

HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", PROJECT_ROOT / "data" / "histdata"))
DEFAULT_ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
                for y in [2020, 2021, 2022, 2023, 2024, 2025]]

TIMEFRAMES = ["M1", "M5", "M15"]

DERIVATIVE_GRID = {
    "smooth_period": [10, 20],
    "d1_period": [2, 4],
    "d2_period": [2],
    "d1_threshold": [0.05, 0.10],
    "d2_threshold": [0.00],
    "sl_atr_mult": [1.5],
    "rr": [2.0, 3.0],
}

FFT_FEATURE_SPECS = [
    (96, 4),    # one hour on M15
    (96, 16),   # four hours on M15
    (192, 16),  # four hours on a two-day window
    (192, 96),  # daily rhythm on a two-day window
]

FILTER_GRID = {
    "fft_line": ["fft_w96_p4", "fft_w96_p16", "fft_w192_p96"],
    "strength_threshold": [1.5, 2.5],
    "filter_action": ["avoid", "reduce"],
}


class FFTClockData(bt.feeds.PandasData):
    lines = tuple(FILTER_GRID["fft_line"])
    params = (
        ("datetime", None),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", -1),
        *tuple((line, line) for line in FILTER_GRID["fft_line"]),
    )


class FFTClockFilteredDerivativeStrategy(bt.Strategy):
    params = (
        ("smooth_period", 20),
        ("d1_period", 2),
        ("d2_period", 2),
        ("d1_threshold", 0.05),
        ("d2_threshold", 0.0),
        ("sl_atr_mult", 1.0),
        ("rr", 2.0),
        ("risk_per_trade", 0.01),
        ("leverage", 30.0),
        ("fft_line", "fft_w96_p4"),
        ("strength_threshold", 2.0),
        ("persistence_bars", 8),
        ("persistence_min", 0.5),
        ("filter_action", "avoid"),
        ("reduce_factor", 0.5),
    )

    def __init__(self) -> None:
        self.ema = bt.ind.EMA(self.data.close, period=self.p.smooth_period)
        self.atr = bt.ind.ATR(self.data, period=14)
        self.entry_order: bt.Order | None = None
        self.stop_order: bt.Order | None = None
        self.target_order: bt.Order | None = None
        self.pending_direction: str | None = None
        self.pending_risk_mult = 1.0

    def _min_bars(self) -> int:
        return max(self.p.smooth_period, 14) + self.p.d1_period + self.p.d2_period + self.p.persistence_bars + 2

    def _calc_d1(self, offset: int) -> float | None:
        atr_value = float(self.atr[offset])
        if math.isnan(atr_value) or atr_value <= 0:
            return None
        return (float(self.ema[offset]) - float(self.ema[offset - self.p.d1_period])) / atr_value

    def _calc_d2(self, offset: int) -> float | None:
        d1_now = self._calc_d1(offset)
        d1_prev = self._calc_d1(offset - self.p.d2_period)
        if d1_now is None or d1_prev is None:
            return None
        return d1_now - d1_prev

    def _has_pending_orders(self) -> bool:
        return any(order is not None for order in (self.entry_order, self.stop_order, self.target_order))

    def _clock_driven(self) -> bool:
        line = getattr(self.data, self.p.fft_line)
        hits = 0
        valid = 0
        for offset in range(0, int(self.p.persistence_bars)):
            value = float(line[-offset])
            if math.isnan(value):
                continue
            valid += 1
            if value >= float(self.p.strength_threshold):
                hits += 1
        if valid <= 0:
            return False
        return (hits / valid) >= float(self.p.persistence_min)

    def _calc_size(self, stop_distance: float, risk_mult: float) -> int:
        account_value = float(self.broker.getvalue())
        cash_risk = account_value * float(self.p.risk_per_trade) * risk_mult
        risk_size = int(cash_risk / stop_distance) if stop_distance > 0 else 0

        current_price = float(self.data.close[0])
        max_size = int((account_value * float(self.p.leverage)) / current_price) if current_price > 0 else 0
        return max(0, min(risk_size, max_size))

    def _submit_entry(self, direction: str, risk_mult: float) -> None:
        atr_value = float(self.atr[0])
        if math.isnan(atr_value) or atr_value <= 0:
            return

        stop_distance = atr_value * float(self.p.sl_atr_mult)
        size = self._calc_size(stop_distance, risk_mult)
        if size <= 0:
            return

        self.pending_direction = direction
        self.pending_risk_mult = risk_mult
        if direction == "long":
            self.entry_order = self.buy(size=size)
        else:
            self.entry_order = self.sell(size=size)

    def next(self) -> None:
        if len(self) < self._min_bars():
            return
        if self.position or self._has_pending_orders():
            return

        clock_driven = self._clock_driven()
        if clock_driven and self.p.filter_action == "avoid":
            return

        d1_now = self._calc_d1(0)
        d1_prev = self._calc_d1(-1)
        d2_now = self._calc_d2(0)
        if d1_now is None or d1_prev is None or d2_now is None:
            return

        risk_mult = float(self.p.reduce_factor) if clock_driven and self.p.filter_action == "reduce" else 1.0
        long_cross = d1_prev <= self.p.d1_threshold and d1_now > self.p.d1_threshold
        short_cross = d1_prev >= -self.p.d1_threshold and d1_now < -self.p.d1_threshold

        if long_cross and d2_now > self.p.d2_threshold:
            self._submit_entry("long", risk_mult)
        elif short_cross and d2_now < -self.p.d2_threshold:
            self._submit_entry("short", risk_mult)

    def notify_order(self, order: bt.Order) -> None:
        if order.status in (bt.Order.Submitted, bt.Order.Accepted):
            return

        if order == self.entry_order:
            if order.status == bt.Order.Completed:
                atr_value = float(self.atr[0])
                stop_distance = atr_value * float(self.p.sl_atr_mult)
                if self.position.size > 0:
                    stop_price = order.executed.price - stop_distance
                    target_price = order.executed.price + stop_distance * float(self.p.rr)
                    self.stop_order = self.sell(size=self.position.size, exectype=bt.Order.Stop, price=stop_price)
                    self.target_order = self.sell(
                        size=self.position.size,
                        exectype=bt.Order.Limit,
                        price=target_price,
                        oco=self.stop_order,
                    )
                elif self.position.size < 0:
                    size = abs(self.position.size)
                    stop_price = order.executed.price + stop_distance
                    target_price = order.executed.price - stop_distance * float(self.p.rr)
                    self.stop_order = self.buy(size=size, exectype=bt.Order.Stop, price=stop_price)
                    self.target_order = self.buy(
                        size=size,
                        exectype=bt.Order.Limit,
                        price=target_price,
                        oco=self.stop_order,
                    )

            if order.status in (bt.Order.Completed, bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected):
                self.entry_order = None
                if order.status != bt.Order.Completed:
                    self.pending_direction = None
            return

        if order in (self.stop_order, self.target_order):
            if order == self.stop_order and order.status in (
                bt.Order.Completed,
                bt.Order.Canceled,
                bt.Order.Margin,
                bt.Order.Rejected,
            ):
                self.stop_order = None
            if order == self.target_order and order.status in (
                bt.Order.Completed,
                bt.Order.Canceled,
                bt.Order.Margin,
                bt.Order.Rejected,
            ):
                self.target_order = None

            if not self.position and self.stop_order is None and self.target_order is None:
                self.pending_direction = None


@dataclass(frozen=True)
class RunResult:
    params: dict[str, float | int | str]
    metrics: dict[str, float | int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run FFT clock-trigger HFT filter grid.")
    parser.add_argument("--timeframe", choices=TIMEFRAMES, default="M15")
    parser.add_argument("--maxcpus", type=int, default=1)
    parser.add_argument("--limit", type=int, default=None, help="Optional limit for quick validation.")
    return parser.parse_args()


def _fft_strength(window_values: np.ndarray, target_period: int) -> float:
    returns = np.diff(np.log(window_values))
    if len(returns) < 8 or not np.isfinite(returns).all():
        return np.nan
    returns = returns - np.mean(returns)
    spectrum = np.abs(np.fft.rfft(returns))
    if len(spectrum) < 5:
        return np.nan

    target_bin = int(round(len(returns) / target_period))
    target_bin = max(1, min(target_bin, len(spectrum) - 1))
    low = max(1, target_bin - 3)
    high = min(len(spectrum), target_bin + 4)
    neighbors = np.delete(spectrum[low:high], target_bin - low)
    baseline = float(np.mean(neighbors)) if len(neighbors) else float(np.mean(spectrum[1:]))
    if baseline <= 0 or not math.isfinite(baseline):
        return np.nan
    return float(spectrum[target_bin] / baseline)


def add_fft_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    close = enriched["close"]
    for window, period in FFT_FEATURE_SPECS:
        name = f"fft_w{window}_p{period}"
        enriched[name] = close.rolling(window=window, min_periods=window).apply(
            lambda values, p=period: _fft_strength(np.asarray(values, dtype=float), p),
            raw=True,
        )
    return enriched.dropna()


def load_or_build_fft_features(frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    cache_path = DATA_ROOT / f"eurusd_{timeframe.lower()}_fft_clock_features.pkl"
    if cache_path.exists():
        return pd.read_pickle(cache_path)

    enriched = add_fft_features(frame)
    enriched.to_pickle(cache_path)
    return enriched


def iter_grid() -> list[dict[str, float | int | str]]:
    keys = list(DERIVATIVE_GRID) + list(FILTER_GRID)
    values = [DERIVATIVE_GRID.get(key, FILTER_GRID.get(key)) for key in keys]
    return [dict(zip(keys, combo, strict=True)) for combo in itertools.product(*values)]


def run_single(frame: pd.DataFrame, params: dict[str, float | int | str], config: RunConfig) -> RunResult:
    cerebro = bt.Cerebro(optreturn=False, maxcpus=1, stdstats=False)
    cerebro.broker.setcash(config.initial_cash)
    cerebro.broker.setcommission(commission=0.0, leverage=config.leverage)
    cerebro.broker.set_slippage_fixed(
        fixed=config.slippage_per_side,
        slip_open=True,
        slip_limit=True,
        slip_match=True,
        slip_out=False,
    )
    cerebro.adddata(FFTClockData(dataname=frame.copy()))
    cerebro.addanalyzer(TradeStatsAnalyzer, _name="trade_stats")
    cerebro.addstrategy(
        FFTClockFilteredDerivativeStrategy,
        **params,
        risk_per_trade=config.risk_per_trade,
        leverage=config.leverage,
    )
    strategy = cerebro.run()[0]
    metrics = strategy.analyzers.trade_stats.get_analysis()
    return RunResult(params=params, metrics=metrics)


def _prefix_result(result: RunResult, prefix: str) -> dict[str, float | int | str]:
    row = dict(result.params)
    for key, value in result.metrics.items():
        if key in {"gross_profit", "gross_loss"}:
            continue
        row[f"{prefix}_{key}"] = value
    return row


def build_report(frame: pd.DataFrame, report_path: Path, generated_at: str, timeframe: str) -> None:
    top = frame.head(15)
    best = top.iloc[0]
    lines: list[str] = []
    lines.append(f"# FFT Clock Trigger HFT Filter - EURUSD {timeframe}")
    lines.append("")
    lines.append("## Related Notes")
    lines.append("- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]")
    lines.append("- [[../../../Pipeline_01/04_BACKTEST/FFT_ACADEMIC_tests/INDEX]]")
    lines.append("- [[../../../Pipeline_01/00_CORE/00_Regole_Progettazione]]")
    lines.append("- [[../../../Pipeline_01/01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]")
    lines.append("")
    lines.append(f"- Generated: {generated_at}")
    lines.append(f"- Timeframe: {timeframe}")
    lines.append(f"- Combinations: {len(frame)}")
    lines.append("- Train: 2020-01-01 -> 2023-12-31")
    lines.append("- OOS: 2024-01-01 -> 2025-12-31")
    lines.append("- Ranking: OOS Profit Factor desc, OOS Max DD asc, OOS P&L desc")
    lines.append("")
    lines.append("## Best Setup")
    lines.append(f"- FFT line: `{best['fft_line']}`")
    lines.append(f"- Filter action: `{best['filter_action']}`")
    lines.append(f"- Strength threshold: {best['strength_threshold']:.2f}")
    lines.append(f"- Smooth: {int(best['smooth_period'])}")
    lines.append(f"- D1 Period: {int(best['d1_period'])}")
    lines.append(f"- D1 Threshold: {best['d1_threshold']:.2f}")
    lines.append(f"- SL ATR: {best['sl_atr_mult']:.1f}")
    lines.append(f"- RR: {best['rr']:.1f}")
    lines.append(f"- Train PF: {best['train_profit_factor']:.3f}")
    lines.append(f"- OOS PF: {best['oos_profit_factor']:.3f}")
    lines.append(f"- OOS DD %: {best['oos_max_drawdown_pct']:.2f}")
    lines.append(f"- OOS P&L %: {best['oos_pnl_pct']:.2f}")
    lines.append(f"- OOS Trades: {int(best['oos_trades'])}")
    lines.append("")
    lines.append("## Top 15")
    lines.append("")
    lines.append("| Rank | FFT | Action | Thr | Smooth | D1 | D1 Thr | SL | RR | Train PF | OOS PF | OOS DD % | OOS P&L % | OOS Trades |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for rank, row in enumerate(top.itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | `{row.fft_line}` | {row.filter_action} | {row.strength_threshold:.2f} | "
            f"{int(row.smooth_period)} | {int(row.d1_period)} | {row.d1_threshold:.2f} | "
            f"{row.sl_atr_mult:.1f} | {row.rr:.1f} | {row.train_profit_factor:.3f} | "
            f"{row.oos_profit_factor:.3f} | {row.oos_max_drawdown_pct:.2f} | "
            f"{row.oos_pnl_pct:.2f} | {int(row.oos_trades)} |"
        )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    combined_csv = PROJECT_ROOT / "artifacts" / "derivative_backtests" / "data" / "eurusd_m1_2020_2025_combined.csv"
    if combined_csv.exists():
        merged_m1 = pd.read_csv(combined_csv, parse_dates=["datetime"]).set_index("datetime")
    else:
        merged_m1 = load_histdata_zips(DEFAULT_ZIPS)
        combined_csv.parent.mkdir(parents=True, exist_ok=True)
        merged_m1.to_csv(combined_csv)

    tf_df = resample_ohlcv(merged_m1, args.timeframe)
    tf_df = load_or_build_fft_features(tf_df, args.timeframe)
    train_df, oos_df = split_frame(
        tf_df,
        train_start="2020-01-01",
        train_end="2023-12-31 23:59:59",
        oos_start="2024-01-01",
        oos_end="2025-12-31 23:59:59",
    )

    grid = iter_grid()
    if args.limit is not None:
        grid = grid[: args.limit]

    print(f"[{args.timeframe}] train bars={len(train_df)} oos bars={len(oos_df)} combinations={len(grid)}")
    config = RunConfig()
    rows: list[dict[str, float | int | str]] = []

    for idx, params in enumerate(grid, start=1):
        train_result = run_single(train_df, params, config)
        oos_result = run_single(oos_df, params, config)
        row = _prefix_result(train_result, "train")
        row.update({k: v for k, v in _prefix_result(oos_result, "oos").items() if k.startswith("oos_")})
        row["tf"] = args.timeframe
        row["total_trades"] = int(row["train_trades"]) + int(row["oos_trades"])
        rows.append(row)
        if idx % 25 == 0 or idx == len(grid):
            print(f"[{args.timeframe}] completed {idx}/{len(grid)}")

    results = pd.DataFrame(rows)
    ordered = [
        "tf",
        "fft_line",
        "filter_action",
        "strength_threshold",
        "smooth_period",
        "d1_period",
        "d2_period",
        "d1_threshold",
        "d2_threshold",
        "sl_atr_mult",
        "rr",
        "train_trades",
        "train_win_rate",
        "train_profit_factor",
        "train_max_drawdown_pct",
        "train_pnl_pct",
        "oos_trades",
        "oos_win_rate",
        "oos_profit_factor",
        "oos_max_drawdown_pct",
        "oos_pnl_pct",
        "total_trades",
    ]
    results = results[ordered].sort_values(
        by=["oos_profit_factor", "oos_max_drawdown_pct", "oos_pnl_pct"],
        ascending=[False, True, False],
        kind="mergesort",
    ).reset_index(drop=True)

    suffix = args.timeframe.lower()
    csv_path = DATA_ROOT / f"fft_clock_filter_results_{suffix}.csv"
    json_path = DATA_ROOT / f"fft_clock_filter_results_{suffix}.json"
    report_path = REPORT_ROOT / f"fft_clock_filter_report_{suffix}.md"
    metadata_path = DATA_ROOT / f"run_metadata_{suffix}.json"

    results.to_csv(csv_path, index=False)
    results.to_json(json_path, orient="records", indent=2)
    build_report(results, report_path, timestamp, args.timeframe)
    metadata_path.write_text(
        json.dumps(
            {
                "generated_at": timestamp,
                "timeframe": args.timeframe,
                "train_bars": len(train_df),
                "oos_bars": len(oos_df),
                "combinations": len(results),
                "single_process": True,
                "fft_feature_specs": FFT_FEATURE_SPECS,
                "best": results.iloc[0].to_dict(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(f"[{args.timeframe}] best OOS PF={results.iloc[0]['oos_profit_factor']:.3f}")
    print(f"[{args.timeframe}] csv={csv_path}")
    print(f"[{args.timeframe}] report={report_path}")


if __name__ == "__main__":
    main()
