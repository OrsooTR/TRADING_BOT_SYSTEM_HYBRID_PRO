# ATR Channel Breakout — EURUSD M15

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
- TF=M15  EMA=20  ATR_mult=2.5
- SL_mult=1.5  RR=4.0  Session=asian
- Train PF=0.7910  |  OOS PF=1.0938
- OOS DD=64.14%  |  OOS P&L=112.81%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 20 | 2.5 | 1.5 | 4.0 | asian | 0.791 | 1.094 | 64.14 | 112.81 |
| 2 | M15 | 100 | 2.0 | 1.0 | 4.0 | asian | 0.997 | 1.057 | 77.78 | 80.62 |
| 3 | M15 | 100 | 2.0 | 1.5 | 4.0 | asian | 1.051 | 1.044 | 68.20 | 44.04 |
| 4 | M15 | 20 | 2.5 | 1.5 | 3.0 | asian | 0.806 | 1.029 | 70.52 | 10.08 |
| 5 | M15 | 100 | 2.0 | 1.5 | 3.0 | asian | 0.992 | 1.027 | 73.59 | 12.55 |
| 6 | M15 | 100 | 2.5 | 1.5 | 4.0 | asian | 1.014 | 1.022 | 59.20 | -4.67 |
| 7 | M15 | 50 | 2.0 | 1.5 | 3.0 | london | 0.949 | 1.019 | 62.85 | -1.71 |
| 8 | M15 | 100 | 3.0 | 1.5 | 2.0 | london | 0.881 | 1.018 | 52.38 | 3.76 |
| 9 | M15 | 50 | 1.5 | 1.0 | 2.0 | asian | 0.944 | 1.016 | 49.22 | 1.53 |
| 10 | M15 | 100 | 2.5 | 1.5 | 3.0 | asian | 0.894 | 1.015 | 56.81 | -7.12 |
