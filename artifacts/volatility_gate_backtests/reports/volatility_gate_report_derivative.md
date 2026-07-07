# Volatility Regime Gate DERIVATIVE

## Related Notes
- [[../../../Pipeline_01/00_CORE/00_Regole_Progettazione]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/volatility_regime_gate]]
- [[../../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]
- [[../../../Pipeline_01/03_STRATEGIES/TESTED/03_RSI_MeanReversion]]
- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/09_LOGS/esperimenti]]

- Generated: 2026-07-07 18:26:08 UTC
- Train: 2020
- OOS: 2021-2025
- Gate implementation: rolling ATR(14) quantile thresholds (percentile proxy) with no-trade in the middle zone

## Logic
- Base strategy: derivative crosses with ATR-based stop and RR target.
- Gate: allow trades only when ATR is in the upper volatility regime.

## Best Setup
- Strategy family: derivative_high_vol
- TF: M15
- Lookback: 200
- Threshold: 0.80
- OOS delta PF: 0.1367
- OOS gated PF: 0.9837
- OOS base PF: 0.8470
- OOS trade reduction: 80.86%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | derivative_high_vol | M15 | 200 | 0.80 | 0.4483 | 0.1367 | 0.8470 | 0.9837 | 80.86 |
| 2 | derivative_high_vol | M15 | 200 | 0.80 | 0.3657 | 0.1331 | 0.8561 | 0.9892 | 81.82 |
| 3 | derivative_high_vol | M15 | 100 | 0.80 | 0.3202 | 0.1147 | 0.8470 | 0.9617 | 81.81 |
| 4 | derivative_high_vol | M15 | 200 | 0.80 | 0.2997 | 0.1141 | 0.8639 | 0.9780 | 80.86 |
| 5 | derivative_high_vol | M15 | 200 | 0.80 | 0.3341 | 0.1141 | 0.8559 | 0.9700 | 81.67 |
| 6 | derivative_high_vol | M15 | 100 | 0.70 | 0.3527 | 0.1137 | 0.8639 | 0.9776 | 71.68 |
| 7 | derivative_high_vol | M5 | 200 | 0.70 | 0.1131 | 0.1132 | 0.7308 | 0.8440 | 62.53 |
| 8 | derivative_high_vol | M15 | 200 | 0.80 | 0.1786 | 0.1131 | 0.8532 | 0.9663 | 81.82 |
| 9 | derivative_high_vol | M5 | 100 | 0.80 | 0.1140 | 0.1121 | 0.7521 | 0.8642 | 72.67 |
| 10 | derivative_high_vol | M5 | 200 | 0.70 | 0.0996 | 0.1113 | 0.7544 | 0.8657 | 62.53 |
