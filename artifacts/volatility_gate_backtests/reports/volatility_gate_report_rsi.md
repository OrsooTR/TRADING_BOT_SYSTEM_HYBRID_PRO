# Volatility Regime Gate RSI

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
- Lookback: 50
- Threshold: 0.20
- OOS delta PF: inf
- OOS gated PF: inf
- OOS base PF: 0.7943
- OOS trade reduction: 99.66%

## Top 10

| Rank | Family | TF | Lkbk | Thr | Train dPF | OOS dPF | OOS Base PF | OOS Gated PF | OOS Trade Red % |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi_low_vol | M5 | 50 | 0.20 | -2.4286 | inf | 0.7943 | inf | 99.66 |
| 2 | rsi_low_vol | M5 | 100 | 0.20 | -2.4286 | inf | 0.7943 | inf | 99.32 |
| 3 | rsi_low_vol | M5 | 50 | 0.20 | -1.8947 | inf | 0.9638 | inf | 99.66 |
| 4 | rsi_low_vol | M5 | 50 | 0.20 | -1.1667 | inf | 1.0702 | inf | 99.66 |
| 5 | rsi_low_vol | M5 | 200 | 0.20 | -0.9600 | 4.9107 | 1.0893 | 6.0000 | 98.29 |
| 6 | rsi_low_vol | M5 | 200 | 0.20 | -0.8750 | 3.3962 | 1.1038 | 4.5000 | 98.29 |
| 7 | rsi_low_vol | M5 | 50 | 0.30 | -2.4286 | 3.2057 | 0.7943 | 4.0000 | 98.98 |
| 8 | rsi_low_vol | M15 | 50 | 0.30 | 0.0000 | 3.1163 | 0.8837 | 4.0000 | 98.21 |
| 9 | rsi_low_vol | M15 | 200 | 0.20 | -0.8491 | 3.0160 | 0.9840 | 4.0000 | 98.60 |
| 10 | rsi_low_vol | M5 | 100 | 0.20 | -1.1667 | 2.9298 | 1.0702 | 4.0000 | 99.32 |
