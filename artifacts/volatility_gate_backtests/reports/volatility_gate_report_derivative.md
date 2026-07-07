# Volatility Regime Gate DERIVATIVE

## Related Notes
- [[../../../Pipeline_01/00_CORE/00_Regole_Progettazione]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/volatility_regime_gate]]
- [[../../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]
- [[../../../Pipeline_01/03_STRATEGIES/TESTED/03_RSI_MeanReversion]]
- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/09_LOGS/esperimenti]]

- Generated: 2026-05-08 09:32:18 UTC
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
- OOS delta PF: 0.1041
- OOS gated PF: 1.1028
- OOS base PF: 0.9987
- OOS trade reduction: 81.82%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | derivative_high_vol | M15 | 200 | 0.80 | 0.3361 | 0.1041 | 0.9987 | 1.1028 | 81.82 |
| 2 | derivative_high_vol | M15 | 200 | 0.80 | 0.4312 | 0.1001 | 0.9858 | 1.0859 | 80.86 |
| 3 | derivative_high_vol | M15 | 100 | 0.80 | 0.2945 | 0.0882 | 0.9858 | 1.0740 | 81.81 |
| 4 | derivative_high_vol | M15 | 100 | 0.70 | 0.3339 | 0.0874 | 0.9846 | 1.0720 | 71.68 |
| 5 | derivative_high_vol | M15 | 200 | 0.80 | 0.3011 | 0.0857 | 0.9989 | 1.0846 | 81.67 |
| 6 | derivative_high_vol | M15 | 200 | 0.80 | 0.2704 | 0.0828 | 0.9846 | 1.0674 | 80.86 |
| 7 | derivative_high_vol | M15 | 200 | 0.80 | 0.1330 | 0.0807 | 0.9964 | 1.0771 | 81.82 |
| 8 | derivative_high_vol | M15 | 200 | 0.80 | 0.4047 | 0.0801 | 1.0023 | 1.0824 | 80.92 |
| 9 | derivative_high_vol | M15 | 200 | 0.80 | 0.2895 | 0.0741 | 0.9735 | 1.0476 | 81.82 |
| 10 | derivative_high_vol | M5 | 50 | 0.80 | 0.0232 | 0.0701 | 0.9601 | 1.0302 | 71.45 |
