# FFT Clock Trigger HFT Filter - EURUSD M15

## Related Notes
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]
- [[../../../Pipeline_01/04_BACKTEST/FFT_ACADEMIC_tests/INDEX]]
- [[../../../Pipeline_01/00_CORE/00_Regole_Progettazione]]
- [[../../../Pipeline_01/01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]

- Generated: 2026-04-29 09:27:43 UTC
- Timeframe: M15
- Combinations: 1
- Train: 2020-01-01 -> 2023-12-31
- OOS: 2024-01-01 -> 2025-12-31
- Ranking: OOS Profit Factor desc, OOS Max DD asc, OOS P&L desc

## Best Setup
- FFT line: `fft_w96_p4`
- Filter action: `avoid`
- Strength threshold: 1.50
- Smooth: 10
- D1 Period: 2
- D1 Threshold: 0.05
- SL ATR: 1.5
- RR: 2.0
- Train PF: 0.848
- OOS PF: 0.877
- OOS DD %: 39.79
- OOS P&L %: -29.87
- OOS Trades: 344

## Top 15

| Rank | FFT | Action | Thr | Smooth | D1 | D1 Thr | SL | RR | Train PF | OOS PF | OOS DD % | OOS P&L % | OOS Trades |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `fft_w96_p4` | avoid | 1.50 | 10 | 2 | 0.05 | 1.5 | 2.0 | 0.848 | 0.877 | 39.79 | -29.87 | 344 |
