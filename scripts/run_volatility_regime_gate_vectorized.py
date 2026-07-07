from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from itertools import product
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from derivatives_bt.data_utils import load_histdata_zips, resample_ohlcv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "volatility_gate_backtests"
DATA_ROOT = ARTIFACT_ROOT / "data"
REPORT_ROOT = ARTIFACT_ROOT / "reports"

HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", PROJECT_ROOT / "data" / "histdata"))
DEFAULT_ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
                for y in [2020, 2021, 2022, 2023, 2024, 2025]]
COMBINED_CSV = PROJECT_ROOT / "artifacts" / "derivative_backtests" / "data" / "eurusd_m1_2020_2025_combined.csv"

TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S, OOS_E = "2021-01-01", "2025-12-31 23:59:59"
TIMEFRAMES = ["M1", "M5", "M15"]
RISK = 0.01
SPREAD_PIP = float(os.environ.get("SPREAD_PIP", "0.5"))  # costo spread round-trip in pip
SPREAD = SPREAD_PIP * 1e-4
MAX_HOLD_PER_TF = {"M1": 100, "M5": 300, "M15": 200}
VOL_LOOKBACKS = [50, 100, 200]
LOW_VOL_PCTS = [0.20, 0.30]
HIGH_VOL_PCTS = [0.70, 0.80]
MIN_TRAIN_GATED_TRADES = 20
MIN_OOS_GATED_TRADES = 50

DERIVATIVE_GRID = {
    "smooth_period": [20],
    "d1_period": [4, 8],
    "d2_period": [2, 4],
    "d1_threshold": [0.05, 0.10],
    "d2_threshold": [0.00],
    "sl_atr_mult": [1.0, 1.5],
    "rr": [2.0, 3.0, 4.0],
}

RSI_GRID = {
    "rsi_period": [14, 21],
    "ob_level": [70, 80],
    "os_level": [30, 20],
    "entry_mode": ["touch", "cross"],
    "sl_atr_mult": [1.5],
    "rr": [2.0, 3.0, 4.0],
}

DERIVATIVE_PARAM_COLS = [
    "strategy_family",
    "tf",
    "smooth_period",
    "d1_period",
    "d2_period",
    "d1_threshold",
    "d2_threshold",
    "sl_atr_mult",
    "rr",
    "vol_lookback",
    "vol_threshold",
]

RSI_PARAM_COLS = [
    "strategy_family",
    "tf",
    "rsi_period",
    "ob_level",
    "os_level",
    "entry_mode",
    "sl_atr_mult",
    "rr",
    "vol_lookback",
    "vol_threshold",
]


def load_m1(zip_paths: list[str | Path]) -> pd.DataFrame:
    if not all(Path(path).exists() for path in zip_paths):
        # fallback: CSV combinato locale (stesso formato EST degli zip HistData)
        frame = pd.read_csv(COMBINED_CSV, parse_dates=["datetime"], index_col="datetime")
        frame = frame.sort_index()
        return frame[~frame.index.duplicated(keep="last")]
    return load_histdata_zips(zip_paths)


def calc_atr(frame: pd.DataFrame, period: int = 14) -> np.ndarray:
    high = frame["high"].to_numpy(dtype=float)
    low = frame["low"].to_numpy(dtype=float)
    close = frame["close"].to_numpy(dtype=float)
    prev_close = np.roll(close, 1)
    prev_close[0] = close[0]
    true_range = np.maximum(high - low, np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    atr = true_range.copy()
    alpha = 1.0 / period
    for i in range(1, len(true_range)):
        atr[i] = atr[i - 1] * (1.0 - alpha) + true_range[i] * alpha
    return atr


def calc_ema(values: np.ndarray, period: int) -> np.ndarray:
    ema = values.astype(float).copy()
    alpha = 2.0 / (period + 1.0)
    for i in range(1, len(values)):
        ema[i] = values[i] * alpha + ema[i - 1] * (1.0 - alpha)
    return ema


def calc_rsi(values: np.ndarray, period: int) -> np.ndarray:
    delta = np.diff(values, prepend=values[0])
    gains = np.where(delta > 0.0, delta, 0.0)
    losses = np.where(delta < 0.0, -delta, 0.0)

    avg_gain = gains.copy()
    avg_loss = losses.copy()
    alpha = 1.0 / period
    for i in range(1, len(values)):
        avg_gain[i] = avg_gain[i - 1] * (1.0 - alpha) + gains[i] * alpha
        avg_loss[i] = avg_loss[i - 1] * (1.0 - alpha) + losses[i] * alpha

    rs = avg_gain / (avg_loss + 1e-12)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi


def rolling_quantile(values: np.ndarray, window: int, quantile: float) -> np.ndarray:
    series = pd.Series(values)
    return series.rolling(window=window, min_periods=window).quantile(quantile).to_numpy()


def sim_and_metrics(
    entry_bars: np.ndarray,
    directions: np.ndarray,
    entry_price: np.ndarray,
    stop_distance: np.ndarray,
    rr: float,
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    max_hold: int,
) -> dict[str, float | int]:
    count = len(entry_bars)
    if count == 0:
        return {
            "trades": 0,
            "win_rate": 0.0,
            "profit_factor": 0.0,
            "max_drawdown_pct": 0.0,
            "pnl_pct": 0.0,
            "longs": 0,
            "shorts": 0,
            "avg_bars": 0.0,
        }

    total_bars = len(high)
    horizon = min(max_hold, total_bars)
    rows = np.clip(entry_bars[:, None] + np.arange(horizon)[None, :], 0, total_bars - 1)
    highs = high[rows]
    lows = low[rows]

    take_profit = entry_price + directions * rr * stop_distance
    stop_loss = entry_price - directions * stop_distance

    is_long = directions == 1
    is_short = directions == -1
    tp_hit = np.zeros((count, horizon), dtype=bool)
    sl_hit = np.zeros((count, horizon), dtype=bool)

    if is_long.any():
        tp_hit[is_long] = highs[is_long] >= take_profit[is_long, None]
        sl_hit[is_long] = lows[is_long] <= stop_loss[is_long, None]
    if is_short.any():
        tp_hit[is_short] = lows[is_short] <= take_profit[is_short, None]
        sl_hit[is_short] = highs[is_short] >= stop_loss[is_short, None]

    tp_bar = np.where(tp_hit.any(axis=1), np.argmax(tp_hit, axis=1), horizon)
    sl_bar = np.where(sl_hit.any(axis=1), np.argmax(sl_hit, axis=1), horizon)
    # tie-break pessimistico: se TP e SL cadono nella stessa barra conta lo SL
    is_win = (tp_bar < sl_bar) & (tp_bar < horizon)
    is_loss = (sl_bar <= tp_bar) & (sl_bar < horizon)
    # timeout: chiusura mark-to-market sull'ultima barra simulata invece di 0R
    last_bar = np.minimum(entry_bars + horizon - 1, total_bars - 1)
    mtm_r = directions * (close[last_bar] - entry_price) / np.maximum(stop_distance, 1e-12)
    pnl_r = np.where(is_win, rr, np.where(is_loss, -1.0, np.clip(mtm_r, -1.0, rr)))
    # costo spread per trade espresso in R (spread / distanza SL)
    pnl_r = pnl_r - SPREAD / np.maximum(stop_distance, 1e-12)
    exit_bar = np.where(is_win, tp_bar, np.where(is_loss, sl_bar, horizon))

    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    for trade_r in pnl_r:
        equity *= 1.0 + RISK * trade_r
        peak = max(peak, equity)
        max_dd = max(max_dd, (peak - equity) / peak * 100.0)

    gross_profit = float(pnl_r[pnl_r > 0].sum())
    gross_loss = float(abs(pnl_r[pnl_r < 0].sum()))
    if gross_loss > 0.0:
        profit_factor = gross_profit / gross_loss
    elif gross_profit > 0.0:
        profit_factor = float("inf")
    else:
        profit_factor = 0.0

    wins = int(is_win.sum())
    return {
        "trades": int(count),
        "win_rate": round(wins / count * 100.0, 2) if count else 0.0,
        "profit_factor": round(float(profit_factor), 4),
        "max_drawdown_pct": round(float(max_dd), 2),
        "pnl_pct": round((equity - 1.0) * 100.0, 2),
        "longs": int(is_long.sum()),
        "shorts": int(is_short.sum()),
        "avg_bars": round(float(exit_bar.mean()), 1),
    }


def derivative_signal_map(frame: pd.DataFrame) -> dict[tuple, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    close = frame["close"].to_numpy(dtype=float)
    atr = calc_atr(frame)
    signal_map: dict[tuple, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    ema_cache = {period: calc_ema(close, period) for period in DERIVATIVE_GRID["smooth_period"]}

    for params in product(
        DERIVATIVE_GRID["smooth_period"],
        DERIVATIVE_GRID["d1_period"],
        DERIVATIVE_GRID["d2_period"],
        DERIVATIVE_GRID["d1_threshold"],
        DERIVATIVE_GRID["d2_threshold"],
        DERIVATIVE_GRID["sl_atr_mult"],
        DERIVATIVE_GRID["rr"],
    ):
        smooth_period, d1_period, d2_period, d1_threshold, d2_threshold, sl_atr_mult, rr = params
        ema = ema_cache[smooth_period]

        d1 = np.full(len(close), np.nan)
        d1[d1_period:] = (ema[d1_period:] - ema[:-d1_period]) / np.maximum(atr[d1_period:], 1e-12)
        d2 = np.full(len(close), np.nan)
        d2[d1_period + d2_period :] = d1[d1_period + d2_period :] - d1[d1_period : -d2_period]

        d1_prev = np.roll(d1, 1)
        long_sig = (d1_prev <= d1_threshold) & (d1 > d1_threshold) & (d2 > d2_threshold)
        short_sig = (d1_prev >= -d1_threshold) & (d1 < -d1_threshold) & (d2 < -d2_threshold)

        warmup = max(smooth_period, 14) + d1_period + d2_period + 2
        long_sig[:warmup] = False
        short_sig[:warmup] = False

        signal_map[params] = (long_sig, short_sig, atr)
    return signal_map


def rsi_signal_map(frame: pd.DataFrame) -> dict[tuple, tuple[np.ndarray, np.ndarray, np.ndarray]]:
    close = frame["close"].to_numpy(dtype=float)
    atr = calc_atr(frame)
    signal_map: dict[tuple, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    rsi_cache = {period: calc_rsi(close, period) for period in RSI_GRID["rsi_period"]}

    for params in product(
        RSI_GRID["rsi_period"],
        RSI_GRID["ob_level"],
        RSI_GRID["os_level"],
        RSI_GRID["entry_mode"],
        RSI_GRID["sl_atr_mult"],
        RSI_GRID["rr"],
    ):
        rsi_period, ob_level, os_level, entry_mode, sl_atr_mult, rr = params
        if ob_level <= os_level:
            continue

        rsi = rsi_cache[rsi_period]
        prev_rsi = np.roll(rsi, 1)

        if entry_mode == "touch":
            long_sig = (rsi < os_level) & (prev_rsi >= os_level)
            short_sig = (rsi > ob_level) & (prev_rsi <= ob_level)
        else:
            long_sig = (rsi > os_level) & (prev_rsi <= os_level)
            short_sig = (rsi < ob_level) & (prev_rsi >= ob_level)

        warmup = max(rsi_period, 14) + 2
        long_sig[:warmup] = False
        short_sig[:warmup] = False

        signal_map[params] = (long_sig, short_sig, atr)
    return signal_map


def evaluate_signal_set(
    frame: pd.DataFrame,
    long_sig: np.ndarray,
    short_sig: np.ndarray,
    atr: np.ndarray,
    sl_atr_mult: float,
    rr: float,
    gate_mask: np.ndarray | None,
    max_hold: int,
) -> dict[str, float | int]:
    open_prices = frame["open"].to_numpy(dtype=float)
    high = frame["high"].to_numpy(dtype=float)
    low = frame["low"].to_numpy(dtype=float)
    close = frame["close"].to_numpy(dtype=float)
    total_bars = len(frame)

    long_mask = long_sig.copy()
    short_mask = short_sig.copy()
    if gate_mask is not None:
        long_mask &= gate_mask
        short_mask &= gate_mask

    long_idx = np.where(long_mask)[0]
    short_idx = np.where(short_mask)[0]
    all_idx = np.concatenate([long_idx, short_idx])
    all_dir = np.concatenate([np.ones(len(long_idx), dtype=int), -np.ones(len(short_idx), dtype=int)])

    if len(all_idx) == 0:
        return sim_and_metrics(
            entry_bars=np.array([], dtype=int),
            directions=np.array([], dtype=int),
            entry_price=np.array([], dtype=float),
            stop_distance=np.array([], dtype=float),
            rr=rr,
            high=high,
            low=low,
            close=close,
            max_hold=max_hold,
        )

    order = np.argsort(all_idx, kind="stable")
    signal_bars = all_idx[order]
    directions = all_dir[order]
    entry_bars = np.minimum(signal_bars + 1, total_bars - 1)
    entry_price = open_prices[entry_bars]
    stop_distance = sl_atr_mult * atr[signal_bars]
    valid = np.isfinite(stop_distance) & (stop_distance > 0.0)
    return sim_and_metrics(
        entry_bars=entry_bars[valid],
        directions=directions[valid],
        entry_price=entry_price[valid],
        stop_distance=stop_distance[valid],
        rr=rr,
        high=high,
        low=low,
        close=close,
        max_hold=max_hold,
    )


def build_gate_masks(atr: np.ndarray) -> tuple[dict[tuple[int, float], np.ndarray], dict[tuple[int, float], np.ndarray]]:
    low_masks: dict[tuple[int, float], np.ndarray] = {}
    high_masks: dict[tuple[int, float], np.ndarray] = {}
    for lookback in VOL_LOOKBACKS:
        for low_pct in LOW_VOL_PCTS:
            low_threshold = rolling_quantile(atr, lookback, low_pct)
            low_masks[(lookback, low_pct)] = np.isfinite(low_threshold) & (atr <= low_threshold)
        for high_pct in HIGH_VOL_PCTS:
            high_threshold = rolling_quantile(atr, lookback, high_pct)
            high_masks[(lookback, high_pct)] = np.isfinite(high_threshold) & (atr >= high_threshold)
    return low_masks, high_masks


def evaluate_derivative_family(frame: pd.DataFrame, tf: str, split_label: str) -> pd.DataFrame:
    max_hold = MAX_HOLD_PER_TF[tf]
    signal_map = derivative_signal_map(frame)
    any_atr = next(iter(signal_map.values()))[2]
    _, high_masks = build_gate_masks(any_atr)
    rows: list[dict[str, float | int | str]] = []

    for params, (long_sig, short_sig, atr) in signal_map.items():
        smooth_period, d1_period, d2_period, d1_threshold, d2_threshold, sl_atr_mult, rr = params
        base_metrics = evaluate_signal_set(
            frame=frame,
            long_sig=long_sig,
            short_sig=short_sig,
            atr=atr,
            sl_atr_mult=sl_atr_mult,
            rr=rr,
            gate_mask=None,
            max_hold=max_hold,
        )

        for (lookback, high_pct), gate_mask in high_masks.items():
            gated_metrics = evaluate_signal_set(
                frame=frame,
                long_sig=long_sig,
                short_sig=short_sig,
                atr=atr,
                sl_atr_mult=sl_atr_mult,
                rr=rr,
                gate_mask=gate_mask,
                max_hold=max_hold,
            )
            base_trades = int(base_metrics["trades"])
            gated_trades = int(gated_metrics["trades"])
            rows.append(
                {
                    "split": split_label,
                    "strategy_family": "derivative_high_vol",
                    "tf": tf,
                    "smooth_period": smooth_period,
                    "d1_period": d1_period,
                    "d2_period": d2_period,
                    "d1_threshold": d1_threshold,
                    "d2_threshold": d2_threshold,
                    "sl_atr_mult": sl_atr_mult,
                    "rr": rr,
                    "vol_lookback": lookback,
                    "vol_threshold": high_pct,
                    "gate_coverage_pct": round(float(gate_mask.mean() * 100.0), 2),
                    "base_trades": base_trades,
                    "base_win_rate": base_metrics["win_rate"],
                    "base_profit_factor": base_metrics["profit_factor"],
                    "base_max_drawdown_pct": base_metrics["max_drawdown_pct"],
                    "base_pnl_pct": base_metrics["pnl_pct"],
                    "gated_trades": gated_trades,
                    "gated_win_rate": gated_metrics["win_rate"],
                    "gated_profit_factor": gated_metrics["profit_factor"],
                    "gated_max_drawdown_pct": gated_metrics["max_drawdown_pct"],
                    "gated_pnl_pct": gated_metrics["pnl_pct"],
                    "delta_profit_factor": round(
                        float(gated_metrics["profit_factor"]) - float(base_metrics["profit_factor"]), 4
                    ),
                    "delta_drawdown_pct": round(
                        float(gated_metrics["max_drawdown_pct"]) - float(base_metrics["max_drawdown_pct"]), 2
                    ),
                    "delta_pnl_pct": round(float(gated_metrics["pnl_pct"]) - float(base_metrics["pnl_pct"]), 2),
                    "trade_reduction_pct": round(
                        (1.0 - (gated_trades / base_trades)) * 100.0 if base_trades > 0 else 0.0,
                        2,
                    ),
                }
            )
    return pd.DataFrame(rows)


def evaluate_rsi_family(frame: pd.DataFrame, tf: str, split_label: str) -> pd.DataFrame:
    max_hold = MAX_HOLD_PER_TF[tf]
    signal_map = rsi_signal_map(frame)
    any_atr = next(iter(signal_map.values()))[2]
    low_masks, _ = build_gate_masks(any_atr)
    rows: list[dict[str, float | int | str]] = []

    for params, (long_sig, short_sig, atr) in signal_map.items():
        rsi_period, ob_level, os_level, entry_mode, sl_atr_mult, rr = params
        base_metrics = evaluate_signal_set(
            frame=frame,
            long_sig=long_sig,
            short_sig=short_sig,
            atr=atr,
            sl_atr_mult=sl_atr_mult,
            rr=rr,
            gate_mask=None,
            max_hold=max_hold,
        )

        for (lookback, low_pct), gate_mask in low_masks.items():
            gated_metrics = evaluate_signal_set(
                frame=frame,
                long_sig=long_sig,
                short_sig=short_sig,
                atr=atr,
                sl_atr_mult=sl_atr_mult,
                rr=rr,
                gate_mask=gate_mask,
                max_hold=max_hold,
            )
            base_trades = int(base_metrics["trades"])
            gated_trades = int(gated_metrics["trades"])
            rows.append(
                {
                    "split": split_label,
                    "strategy_family": "rsi_low_vol",
                    "tf": tf,
                    "rsi_period": rsi_period,
                    "ob_level": ob_level,
                    "os_level": os_level,
                    "entry_mode": entry_mode,
                    "sl_atr_mult": sl_atr_mult,
                    "rr": rr,
                    "vol_lookback": lookback,
                    "vol_threshold": low_pct,
                    "gate_coverage_pct": round(float(gate_mask.mean() * 100.0), 2),
                    "base_trades": base_trades,
                    "base_win_rate": base_metrics["win_rate"],
                    "base_profit_factor": base_metrics["profit_factor"],
                    "base_max_drawdown_pct": base_metrics["max_drawdown_pct"],
                    "base_pnl_pct": base_metrics["pnl_pct"],
                    "gated_trades": gated_trades,
                    "gated_win_rate": gated_metrics["win_rate"],
                    "gated_profit_factor": gated_metrics["profit_factor"],
                    "gated_max_drawdown_pct": gated_metrics["max_drawdown_pct"],
                    "gated_pnl_pct": gated_metrics["pnl_pct"],
                    "delta_profit_factor": round(
                        float(gated_metrics["profit_factor"]) - float(base_metrics["profit_factor"]), 4
                    ),
                    "delta_drawdown_pct": round(
                        float(gated_metrics["max_drawdown_pct"]) - float(base_metrics["max_drawdown_pct"]), 2
                    ),
                    "delta_pnl_pct": round(float(gated_metrics["pnl_pct"]) - float(base_metrics["pnl_pct"]), 2),
                    "trade_reduction_pct": round(
                        (1.0 - (gated_trades / base_trades)) * 100.0 if base_trades > 0 else 0.0,
                        2,
                    ),
                }
            )
    return pd.DataFrame(rows)


def combine_split_results(frame: pd.DataFrame, param_cols: list[str]) -> pd.DataFrame:
    train = frame[frame["split"] == "train"].drop(columns=["split"]).copy()
    oos = frame[frame["split"] == "oos"].drop(columns=["split"]).copy()
    train = train.rename(columns={col: f"train_{col}" for col in train.columns if col not in param_cols})
    oos = oos.rename(columns={col: f"oos_{col}" for col in oos.columns if col not in param_cols})
    merged = train.merge(oos, on=param_cols, how="inner")
    merged = merged.sort_values(
        by=["oos_delta_profit_factor", "oos_gated_profit_factor", "oos_delta_drawdown_pct"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    return merged


def write_report(label: str, frame: pd.DataFrame, report_path: Path, generated_at: str) -> None:
    if frame.empty:
        report_path.write_text(
            "\n".join(
                [
                    f"# Volatility Regime Gate {label}",
                    "",
                    "No rows matched the selection criteria.",
                    "",
                ]
            ),
            encoding="utf-8",
        )
        return

    top = frame.head(10).copy()
    best = top.iloc[0]
    strategy_family = str(best["strategy_family"])

    lines: list[str] = []
    lines.append(f"# Volatility Regime Gate {label}")
    lines.append("")
    lines.append("## Related Notes")
    lines.append("- [[../../../Pipeline_01/00_CORE/00_Regole_Progettazione]]")
    lines.append("- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/volatility_regime_gate]]")
    lines.append("- [[../../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]")
    lines.append("- [[../../../Pipeline_01/03_STRATEGIES/TESTED/03_RSI_MeanReversion]]")
    lines.append("- [[../../../Pipeline_01/04_BACKTEST/INDEX]]")
    lines.append("- [[../../../Pipeline_01/09_LOGS/esperimenti]]")
    lines.append("")
    lines.append(f"- Generated: {generated_at}")
    lines.append("- Train: 2020")
    lines.append("- OOS: 2021-2025")
    lines.append("- Gate implementation: rolling ATR(14) quantile thresholds (percentile proxy) with no-trade in the middle zone")
    lines.append("")
    lines.append("## Logic")
    if strategy_family == "derivative_high_vol":
        lines.append("- Base strategy: derivative crosses with ATR-based stop and RR target.")
        lines.append("- Gate: allow trades only when ATR is in the upper volatility regime.")
    else:
        lines.append("- Base strategy: RSI mean-reversion with ATR-based stop and RR target.")
        lines.append("- Gate: allow trades only when ATR is in the lower volatility regime.")
    lines.append("")
    lines.append("## Best Setup")
    lines.append(f"- Strategy family: {strategy_family}")
    lines.append(f"- TF: {best['tf']}")
    lines.append(f"- Lookback: {int(best['vol_lookback'])}")
    lines.append(f"- Threshold: {float(best['vol_threshold']):.2f}")
    lines.append(f"- OOS delta PF: {best['oos_delta_profit_factor']:.4f}")
    lines.append(f"- OOS gated PF: {best['oos_gated_profit_factor']:.4f}")
    lines.append(f"- OOS base PF: {best['oos_base_profit_factor']:.4f}")
    lines.append(f"- OOS trade reduction: {best['oos_trade_reduction_pct']:.2f}%")
    lines.append("")
    lines.append("## Top 10")
    lines.append("")
    lines.append("| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    for rank, row in enumerate(top.itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | {row.strategy_family} | {row.tf} | {int(row.vol_lookback)} | {float(row.vol_threshold):.2f} | "
            f"{row.train_delta_profit_factor:.4f} | {row.oos_delta_profit_factor:.4f} | "
            f"{row.oos_base_profit_factor:.4f} | {row.oos_gated_profit_factor:.4f} | {row.oos_trade_reduction_pct:.2f} |"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def robust_subset(frame: pd.DataFrame) -> pd.DataFrame:
    return frame[
        (frame["train_gated_trades"] >= MIN_TRAIN_GATED_TRADES)
        & (frame["oos_gated_trades"] >= MIN_OOS_GATED_TRADES)
    ].copy()


def main() -> None:
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    print("Loading EURUSD M1 zip data...")
    m1 = load_m1(DEFAULT_ZIPS)
    print(f"Loaded {len(m1)} M1 bars.")

    derivative_outputs: list[pd.DataFrame] = []
    rsi_outputs: list[pd.DataFrame] = []

    for tf in TIMEFRAMES:
        print(f"\n[{tf}] Preparing split frames...")
        tf_frame = resample_ohlcv(m1, tf)
        train = tf_frame.loc[TRAIN_S:TRAIN_E].copy()
        oos = tf_frame.loc[OOS_S:OOS_E].copy()
        print(f"  Train bars: {len(train)} | OOS bars: {len(oos)}")

        derivative_split_results = pd.concat(
            [
                evaluate_derivative_family(train, tf, "train"),
                evaluate_derivative_family(oos, tf, "oos"),
            ],
            ignore_index=True,
        )
        derivative_combined = combine_split_results(derivative_split_results, DERIVATIVE_PARAM_COLS)
        derivative_outputs.append(derivative_combined)
        derivative_path = DATA_ROOT / f"volatility_gate_derivative_{tf.lower()}.csv"
        derivative_combined.to_csv(derivative_path, index=False)
        print(
            "  Derivative high-vol best OOS delta PF:",
            f"{derivative_combined.iloc[0]['oos_delta_profit_factor']:.4f}",
        )

        rsi_split_results = pd.concat(
            [
                evaluate_rsi_family(train, tf, "train"),
                evaluate_rsi_family(oos, tf, "oos"),
            ],
            ignore_index=True,
        )
        rsi_combined = combine_split_results(rsi_split_results, RSI_PARAM_COLS)
        rsi_outputs.append(rsi_combined)
        rsi_path = DATA_ROOT / f"volatility_gate_rsi_{tf.lower()}.csv"
        rsi_combined.to_csv(rsi_path, index=False)
        print("  RSI low-vol best OOS delta PF:", f"{rsi_combined.iloc[0]['oos_delta_profit_factor']:.4f}")

    derivative_all = pd.concat(derivative_outputs, ignore_index=True).sort_values(
        by=["oos_delta_profit_factor", "oos_gated_profit_factor", "oos_delta_drawdown_pct"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    derivative_all.to_csv(DATA_ROOT / "volatility_gate_derivative_all.csv", index=False)

    rsi_all = pd.concat(rsi_outputs, ignore_index=True).sort_values(
        by=["oos_delta_profit_factor", "oos_gated_profit_factor", "oos_delta_drawdown_pct"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    rsi_all.to_csv(DATA_ROOT / "volatility_gate_rsi_all.csv", index=False)

    combined_all = pd.concat([derivative_all, rsi_all], ignore_index=True).sort_values(
        by=["oos_delta_profit_factor", "oos_gated_profit_factor", "oos_delta_drawdown_pct"],
        ascending=[False, False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    combined_all.to_csv(DATA_ROOT / "volatility_gate_all.csv", index=False)
    combined_all.to_json(DATA_ROOT / "volatility_gate_all.json", orient="records", indent=2)

    derivative_robust = robust_subset(derivative_all).reset_index(drop=True)
    rsi_robust = robust_subset(rsi_all).reset_index(drop=True)
    combined_robust = robust_subset(combined_all).reset_index(drop=True)
    derivative_robust.to_csv(DATA_ROOT / "volatility_gate_derivative_robust.csv", index=False)
    rsi_robust.to_csv(DATA_ROOT / "volatility_gate_rsi_robust.csv", index=False)
    combined_robust.to_csv(DATA_ROOT / "volatility_gate_all_robust.csv", index=False)

    metadata = {
        "generated_at": generated_at,
        "split": {"train": [TRAIN_S, TRAIN_E], "oos": [OOS_S, OOS_E]},
        "timeframes": TIMEFRAMES,
        "vol_lookbacks": VOL_LOOKBACKS,
        "low_vol_percentiles": LOW_VOL_PCTS,
        "high_vol_percentiles": HIGH_VOL_PCTS,
        "robust_filters": {
            "min_train_gated_trades": MIN_TRAIN_GATED_TRADES,
            "min_oos_gated_trades": MIN_OOS_GATED_TRADES,
        },
        "derivative_grid_size": int(np.prod([len(v) for v in DERIVATIVE_GRID.values()])),
        "rsi_grid_size": int(np.prod([len(v) for v in RSI_GRID.values()])),
    }
    (DATA_ROOT / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    write_report("ALL", combined_all, REPORT_ROOT / "volatility_gate_report_all.md", generated_at)
    write_report("DERIVATIVE", derivative_all, REPORT_ROOT / "volatility_gate_report_derivative.md", generated_at)
    write_report("RSI", rsi_all, REPORT_ROOT / "volatility_gate_report_rsi.md", generated_at)
    write_report("ALL ROBUST", combined_robust, REPORT_ROOT / "volatility_gate_report_all_robust.md", generated_at)
    write_report(
        "DERIVATIVE ROBUST",
        derivative_robust,
        REPORT_ROOT / "volatility_gate_report_derivative_robust.md",
        generated_at,
    )
    write_report("RSI ROBUST", rsi_robust, REPORT_ROOT / "volatility_gate_report_rsi_robust.md", generated_at)

    print("\nVolatility regime gate backtests completed.")
    print(
        "Rows written:"
        f" derivative={len(derivative_all)}"
        f" | rsi={len(rsi_all)}"
        f" | all={len(combined_all)}"
        f" | robust={len(combined_robust)}"
    )


if __name__ == "__main__":
    main()
