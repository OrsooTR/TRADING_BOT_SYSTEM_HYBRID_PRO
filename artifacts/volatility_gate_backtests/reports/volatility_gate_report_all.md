# Volatility Regime Gate ALL

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
- TF: M5
- Lookback: 50
- Threshold: 0.20
- OOS delta PF: inf
- OOS gated PF: inf
- OOS base PF: 0.7160
- OOS trade reduction: 99.66%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi_low_vol | M5 | 50 | 0.20 | -2.1663 | inf | 0.7160 | inf | 99.66 |
| 2 | rsi_low_vol | M5 | 100 | 0.20 | -2.1663 | inf | 0.7160 | inf | 99.32 |
| 3 | rsi_low_vol | M5 | 50 | 0.20 | -1.7157 | inf | 0.8632 | inf | 99.66 |
| 4 | rsi_low_vol | M5 | 50 | 0.20 | -1.0596 | inf | 0.9933 | inf | 99.66 |
| 5 | rsi_low_vol | M5 | 200 | 0.20 | -0.8731 | 3.8727 | 1.0296 | 4.9023 | 98.29 |
| 6 | rsi_low_vol | M15 | 50 | 0.30 | 0.0000 | 2.7759 | 0.9806 | 3.7565 | 98.21 |
| 7 | rsi_low_vol | M5 | 50 | 0.30 | -2.1663 | 2.7564 | 0.7160 | 3.4724 | 98.98 |
| 8 | rsi_low_vol | M5 | 200 | 0.20 | -0.7896 | 2.6250 | 0.9978 | 3.6228 | 98.29 |
| 9 | rsi_low_vol | M5 | 50 | 0.20 | -0.8731 | 2.5847 | 1.0296 | 3.6143 | 98.63 |
| 10 | rsi_low_vol | M15 | 200 | 0.20 | -0.8046 | 2.5259 | 0.9295 | 3.4554 | 98.60 |
