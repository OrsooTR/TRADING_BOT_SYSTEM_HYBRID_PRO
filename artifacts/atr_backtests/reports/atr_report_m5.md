# ATR Channel Breakout — EURUSD M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-05-08 07:44:47 UTC  |  Combinations: 288
- Train: 2020-2023  |  OOS: 2024-2025

## Logic
- Channel: EMA(ema_period) ± atr_channel_mult × ATR(14)
- Long:  prev_close ≤ upper  AND  close > upper
- Short: prev_close ≥ lower  AND  close < lower
- Entry: next-bar open  |  SL: ±sl_mult×ATR  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M5  EMA=100  ATR_mult=1.5
- SL_mult=1.0  RR=4.0  Session=asian
- Train PF=1.0031  |  OOS PF=1.0353
- OOS DD=92.01%  |  OOS P&L=87.86%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 100 | 1.5 | 1.0 | 4.0 | asian | 1.003 | 1.035 | 92.01 | 87.86 |
| 2 | M5 | 100 | 1.5 | 1.0 | 3.0 | asian | 0.980 | 1.032 | 86.09 | 98.13 |
| 3 | M5 | 100 | 2.0 | 1.0 | 3.0 | asian | 0.990 | 1.025 | 90.10 | 28.17 |
| 4 | M5 | 100 | 2.0 | 1.0 | 2.0 | asian | 0.988 | 1.020 | 76.60 | 29.43 |
| 5 | M5 | 100 | 2.0 | 1.0 | 4.0 | asian | 0.967 | 1.012 | 93.50 | -53.49 |
| 6 | M5 | 100 | 1.5 | 1.0 | 2.0 | asian | 1.023 | 1.011 | 82.96 | -18.67 |
| 7 | M5 | 100 | 1.5 | 1.5 | 2.0 | asian | 0.930 | 1.011 | 87.85 | -18.67 |
| 8 | M5 | 100 | 2.0 | 1.5 | 2.0 | asian | 0.956 | 1.010 | 89.05 | -22.08 |
| 9 | M5 | 100 | 2.0 | 1.5 | 4.0 | asian | 0.900 | 1.008 | 96.18 | -61.03 |
| 10 | M5 | 50 | 1.5 | 1.0 | 2.0 | asian | 1.011 | 1.006 | 88.98 | -42.87 |
