# Volatility Regime Gate RSI ROBUST

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
- Base strategy: RSI mean-reversion with ATR-based stop and RR target.
- Gate: allow trades only when ATR is in the lower volatility regime.

## Best Setup
- Strategy family: rsi_low_vol
- TF: M5
- Lookback: 200
- Threshold: 0.30
- OOS delta PF: 0.3286
- OOS gated PF: 1.3973
- OOS base PF: 1.0687
- OOS trade reduction: 79.84%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi_low_vol | M5 | 200 | 0.30 | -0.1985 | 0.3286 | 1.0687 | 1.3973 | 79.84 |
| 2 | rsi_low_vol | M5 | 200 | 0.30 | -0.0741 | 0.3105 | 1.0123 | 1.3228 | 82.85 |
| 3 | rsi_low_vol | M1 | 100 | 0.20 | 0.1585 | 0.2979 | 1.0839 | 1.3818 | 90.99 |
| 4 | rsi_low_vol | M1 | 50 | 0.30 | 0.4064 | 0.2944 | 1.0329 | 1.3273 | 90.87 |
| 5 | rsi_low_vol | M1 | 100 | 0.20 | 0.1771 | 0.2851 | 1.0329 | 1.3180 | 90.99 |
| 6 | rsi_low_vol | M1 | 50 | 0.20 | 0.5540 | 0.2772 | 1.0329 | 1.3101 | 94.09 |
| 7 | rsi_low_vol | M5 | 200 | 0.20 | -0.2304 | 0.2714 | 1.0143 | 1.2857 | 92.13 |
| 8 | rsi_low_vol | M1 | 50 | 0.30 | 0.2854 | 0.2672 | 1.0839 | 1.3511 | 90.87 |
| 9 | rsi_low_vol | M1 | 50 | 0.20 | 0.1703 | 0.2606 | 1.0360 | 1.2966 | 89.64 |
| 10 | rsi_low_vol | M1 | 100 | 0.20 | -0.0028 | 0.2600 | 1.0360 | 1.2960 | 87.57 |
