from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from derivatives_bt.backtest import RunConfig
from derivatives_bt.data_utils import load_histdata_zips, resample_ohlcv, split_frame
from derivatives_bt.session_vwap import VWAP_PARAM_COLS, add_session_vwap_features, run_vwap_optimization


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_ROOT = PROJECT_ROOT / "artifacts" / "vwap_backtests"
DATA_ROOT = ARTIFACT_ROOT / "data"
REPORT_ROOT = ARTIFACT_ROOT / "reports"

HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", PROJECT_ROOT / "data" / "histdata"))
DEFAULT_ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
                for y in [2020, 2021, 2022, 2023, 2024, 2025]]

FULL_GRID = {
    "session_label": ["day", "london", "newyork"],
    "min_session_bars": [15, 30, 45],
    "entry_atr_mult": [1.5, 2.0, 2.5],
    "rejection_frac": [0.25, 0.50],
    "sl_atr_mult": [1.0, 1.5],
    "rr": [2.0, 3.0, 4.0],
}

FOCUSED_GRID = {
    "session_label": ["day", "london", "newyork"],
    "min_session_bars": [30, 45],
    "entry_atr_mult": [1.5, 2.0],
    "rejection_frac": [0.25, 0.50],
    "sl_atr_mult": [1.0, 1.5],
    "rr": [2.0, 3.0, 4.0],
}

SMOKE_GRID = {
    "session_label": ["day"],
    "min_session_bars": [30],
    "entry_atr_mult": [1.5, 2.0],
    "rejection_frac": [0.25],
    "sl_atr_mult": [1.0],
    "rr": [2.0, 3.0],
}

TIMEFRAMES = ["M1", "M5", "M15"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run EUR/USD VWAP session mean-reversion grid search.")
    parser.add_argument("--smoke", action="store_true", help="Run a minimal validation subset.")
    parser.add_argument(
        "--grid-profile",
        choices=["focused", "full"],
        default="full",
        help="Choose the parameter grid. Ignored when --smoke is used.",
    )
    parser.add_argument("--maxcpus", type=int, default=None, help="Override Backtrader maxcpus.")
    parser.add_argument(
        "--timeframes",
        nargs="+",
        default=TIMEFRAMES,
        choices=TIMEFRAMES,
        help="Subset of timeframes to process.",
    )
    return parser.parse_args()


def _prefix_metrics(frame: pd.DataFrame, prefix: str) -> pd.DataFrame:
    return frame.rename(
        columns={
            "trades": f"{prefix}_trades",
            "win_rate": f"{prefix}_win_rate",
            "profit_factor": f"{prefix}_profit_factor",
            "max_drawdown_pct": f"{prefix}_max_drawdown_pct",
            "pnl_pct": f"{prefix}_pnl_pct",
            "longs": f"{prefix}_longs",
            "shorts": f"{prefix}_shorts",
            "avg_bars": f"{prefix}_avg_bars",
        }
    )


def _weighted_average(values: pd.Series, weights: pd.Series) -> float:
    total_weight = float(weights.sum())
    if total_weight <= 0:
        return 0.0
    return float((values * weights).sum() / total_weight)


def build_combined_results(
    timeframe: str,
    train_results: list[dict[str, str | float | int]],
    oos_results: list[dict[str, str | float | int]],
) -> pd.DataFrame:
    train_df = _prefix_metrics(pd.DataFrame(train_results), "train")
    oos_df = _prefix_metrics(pd.DataFrame(oos_results), "oos")

    merged = train_df.merge(oos_df, on=VWAP_PARAM_COLS, how="inner")
    merged.insert(0, "tf", timeframe)
    merged["total_longs"] = merged["train_longs"] + merged["oos_longs"]
    merged["total_shorts"] = merged["train_shorts"] + merged["oos_shorts"]
    merged["total_trades"] = merged["train_trades"] + merged["oos_trades"]
    merged["avg_bars"] = merged.apply(
        lambda row: _weighted_average(
            pd.Series([row["train_avg_bars"], row["oos_avg_bars"]]),
            pd.Series([row["train_trades"], row["oos_trades"]]),
        ),
        axis=1,
    )
    merged = merged.drop(
        columns=[
            "train_longs",
            "train_shorts",
            "train_avg_bars",
            "oos_longs",
            "oos_shorts",
            "oos_avg_bars",
        ]
    )
    merged = merged.sort_values(
        by=["oos_profit_factor", "oos_max_drawdown_pct", "oos_pnl_pct"],
        ascending=[False, True, False],
        kind="mergesort",
    ).reset_index(drop=True)
    return merged


def format_for_export(frame: pd.DataFrame) -> pd.DataFrame:
    ordered_cols = [
        "tf",
        "session_label",
        "min_session_bars",
        "entry_atr_mult",
        "rejection_frac",
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
        "total_longs",
        "total_shorts",
        "avg_bars",
    ]
    return frame[ordered_cols]


def create_markdown_report(
    timeframe_label: str,
    frame: pd.DataFrame,
    report_path: Path,
    generated_at: str,
    mode_label: str,
) -> None:
    top = frame.head(10).copy()
    best = top.iloc[0]
    lines: list[str] = []
    lines.append(f"# Backtest VWAP Session Mean Reversion EURUSD {timeframe_label}")
    lines.append("")
    lines.append("## Related Notes")
    lines.append("- [[../../../Pipeline_01/04_BACKTEST/INDEX]]")
    lines.append("- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]")
    lines.append("- [[../../../Pipeline_01/09_LOGS/esperimenti]]")
    lines.append("- [[../../../Pipeline_01/11_MEMORY/PROJECT_STATE]]")
    lines.append("")
    lines.append(f"- Generated: {generated_at}")
    lines.append(f"- Mode: {mode_label}")
    lines.append(f"- Combinations: {len(frame)}")
    lines.append("- Ranking: OOS Profit Factor desc, OOS Max DD asc, OOS P&L desc")
    lines.append("")
    lines.append("## Logic")
    lines.append("- Trigger long: close extends below session VWAP by ATR band and the candle rejects the lows.")
    lines.append("- Trigger short: close extends above session VWAP by ATR band and the candle rejects the highs.")
    lines.append("- Stop: ATR x sl_atr_mult")
    lines.append("- Target: min(session VWAP room, stop x RR), with minimum room >= 2R")
    lines.append("")
    lines.append("## Best Setup")
    lines.append(f"- TF: {best['tf']}")
    lines.append(f"- Session: {best['session_label']}")
    lines.append(f"- Min Session Bars: {int(best['min_session_bars'])}")
    lines.append(f"- Entry ATR Mult: {best['entry_atr_mult']:.2f}")
    lines.append(f"- Rejection Fraction: {best['rejection_frac']:.2f}")
    lines.append(f"- SL ATR: {best['sl_atr_mult']:.2f}")
    lines.append(f"- RR Cap: {best['rr']:.1f}")
    lines.append(f"- Train PF: {best['train_profit_factor']:.3f}")
    lines.append(f"- OOS PF: {best['oos_profit_factor']:.3f}")
    lines.append(f"- OOS DD %: {best['oos_max_drawdown_pct']:.2f}")
    lines.append(f"- OOS P&L %: {best['oos_pnl_pct']:.2f}")
    lines.append("")
    lines.append("## Top 10")
    lines.append("")
    lines.append("| Rank | TF | Session | Bars | Entry ATR | Reject | SL ATR | RR | Train PF | OOS PF | OOS DD % | OOS P&L % |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for rank, row in enumerate(top.itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | {row.tf} | {row.session_label} | {int(row.min_session_bars)} | "
            f"{row.entry_atr_mult:.2f} | {row.rejection_frac:.2f} | {row.sl_atr_mult:.2f} | {row.rr:.1f} | "
            f"{row.train_profit_factor:.3f} | {row.oos_profit_factor:.3f} | {row.oos_max_drawdown_pct:.2f} | {row.oos_pnl_pct:.2f} |"
        )

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_metadata(metadata: dict[str, object], output_path: Path) -> None:
    output_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main() -> None:
    args = parse_args()
    if args.smoke:
        grid = SMOKE_GRID
        grid_label = "smoke"
    elif args.grid_profile == "focused":
        grid = FOCUSED_GRID
        grid_label = "focused"
    else:
        grid = FULL_GRID
        grid_label = "full"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    DATA_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    merged_m1 = load_histdata_zips(DEFAULT_ZIPS)
    merged_m1.to_csv(DATA_ROOT / "eurusd_m1_2020_2025_combined.csv")

    full_results: list[pd.DataFrame] = []
    metadata: dict[str, object] = {
        "generated_at": timestamp,
        "mode": grid_label,
        "zip_paths": [str(path) for path in DEFAULT_ZIPS],
        "timeframes": {},
    }
    config = RunConfig()

    for timeframe in args.timeframes:
        timeframe_df = resample_ohlcv(merged_m1, timeframe)
        timeframe_df = add_session_vwap_features(timeframe_df)
        if args.smoke:
            train_df, oos_df = split_frame(
                timeframe_df,
                train_start="2020-01-01",
                train_end="2020-03-31 23:59:59",
                oos_start="2024-01-01",
                oos_end="2024-03-31 23:59:59",
            )
        else:
            train_df, oos_df = split_frame(
                timeframe_df,
                train_start="2020-01-01",
                train_end="2023-12-31 23:59:59",
                oos_start="2024-01-01",
                oos_end="2025-12-31 23:59:59",
            )

        print(f"[{timeframe}] train bars={len(train_df)} oos bars={len(oos_df)}")
        train_results = run_vwap_optimization(train_df, grid, config=config, maxcpus=args.maxcpus)
        print(f"[{timeframe}] train complete -> {len(train_results)} combinations")
        oos_results = run_vwap_optimization(oos_df, grid, config=config, maxcpus=args.maxcpus)
        print(f"[{timeframe}] oos complete -> {len(oos_results)} combinations")

        combined = build_combined_results(timeframe, train_results, oos_results)
        combined = format_for_export(combined)
        full_results.append(combined)
        combined.to_csv(
            DATA_ROOT / f"vwap_session_results_{timeframe.lower()}_{'smoke' if args.smoke else grid_label}.csv",
            index=False,
        )

        metadata["timeframes"][timeframe] = {
            "rows": int(len(combined)),
            "train_bars": int(len(train_df)),
            "oos_bars": int(len(oos_df)),
            "best_oos_pf": float(combined.iloc[0]["oos_profit_factor"]),
            "best_oos_dd_pct": float(combined.iloc[0]["oos_max_drawdown_pct"]),
        }

    results_df = pd.concat(full_results, ignore_index=True)
    results_df = results_df.sort_values(
        by=["oos_profit_factor", "oos_max_drawdown_pct", "oos_pnl_pct"],
        ascending=[False, True, False],
        kind="mergesort",
    ).reset_index(drop=True)

    suffix = "smoke" if args.smoke else grid_label
    results_csv = DATA_ROOT / f"vwap_session_results_{suffix}.csv"
    results_json = DATA_ROOT / f"vwap_session_results_{suffix}.json"
    results_df.to_csv(results_csv, index=False)
    results_df.to_json(results_json, orient="records", indent=2)
    save_metadata(metadata, DATA_ROOT / f"run_metadata_{suffix}.json")

    create_markdown_report(
        timeframe_label="ALL_TFS",
        frame=results_df,
        report_path=REPORT_ROOT / f"vwap_session_report_all_tfs_{suffix}.md",
        generated_at=timestamp,
        mode_label=grid_label,
    )
    for timeframe in args.timeframes:
        create_markdown_report(
            timeframe_label=timeframe,
            frame=results_df[results_df["tf"] == timeframe].reset_index(drop=True),
            report_path=REPORT_ROOT / f"vwap_session_report_{timeframe.lower()}_{suffix}.md",
            generated_at=timestamp,
            mode_label=grid_label,
        )


if __name__ == "__main__":
    main()
