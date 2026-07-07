# Volatility Regime Gate RSI ROBUST

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
- Base strategy: RSI mean-reversion with ATR-based stop and RR target.
- Gate: allow trades only when ATR is in the lower volatility regime.

## Best Setup
- Strategy family: rsi_low_vol
- TF: M15
- Lookback: 100
- Threshold: 0.30
- OOS delta PF: 0.1946
- OOS gated PF: 1.1075
- OOS base PF: 0.9129
- OOS trade reduction: 91.56%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi_low_vol | M15 | 100 | 0.30 | -0.5346 | 0.1946 | 0.9129 | 1.1075 | 91.56 |
| 2 | rsi_low_vol | M5 | 200 | 0.30 | -0.2003 | 0.1811 | 0.9182 | 1.0993 | 79.84 |
| 3 | rsi_low_vol | M5 | 200 | 0.30 | -0.1113 | 0.1445 | 0.8822 | 1.0267 | 82.85 |
| 4 | rsi_low_vol | M5 | 200 | 0.20 | -0.2640 | 0.1430 | 0.8941 | 1.0371 | 92.13 |
| 5 | rsi_low_vol | M15 | 100 | 0.30 | -0.5659 | 0.1392 | 0.9107 | 1.0499 | 91.56 |
| 6 | rsi_low_vol | M15 | 200 | 0.20 | -0.2937 | 0.1121 | 0.9347 | 1.0468 | 91.95 |
| 7 | rsi_low_vol | M5 | 50 | 0.30 | -0.1122 | 0.0852 | 0.8773 | 0.9625 | 79.19 |
| 8 | rsi_low_vol | M15 | 100 | 0.20 | -0.4561 | 0.0844 | 0.9347 | 1.0191 | 91.79 |
| 9 | rsi_low_vol | M15 | 200 | 0.20 | 0.0812 | 0.0824 | 0.9002 | 0.9826 | 91.95 |
| 10 | rsi_low_vol | M5 | 200 | 0.30 | -0.1122 | 0.0823 | 0.8527 | 0.9350 | 85.03 |
