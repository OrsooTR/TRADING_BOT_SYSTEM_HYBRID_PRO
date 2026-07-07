# ATR Channel Breakout — EURUSD M15

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-07-07 18:21:17 UTC  |  Combinations: 288
- Train: 2020  |  OOS: 2021-2025

## Logic
- Channel: EMA(ema_period) ± atr_channel_mult × ATR(14)
- Long:  prev_close ≤ upper  AND  close > upper
- Short: prev_close ≥ lower  AND  close < lower
- Entry: next-bar open  |  SL: ±sl_mult×ATR  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M15  EMA=20  ATR_mult=2.5
- SL_mult=1.5  RR=4.0  Session=london
- Train PF=0.8298  |  OOS PF=0.9912
- OOS DD=81.05%  |  OOS P&L=-40.78%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 20 | 2.5 | 1.5 | 4.0 | london | 0.830 | 0.991 | 81.05 | -40.78 |
| 2 | M15 | 20 | 3.0 | 1.0 | 3.0 | newyork | 0.683 | 0.969 | 47.36 | -20.79 |
| 3 | M15 | 50 | 2.0 | 1.5 | 3.0 | newyork | 0.881 | 0.961 | 72.73 | -63.82 |
| 4 | M15 | 20 | 3.0 | 1.5 | 4.0 | newyork | 1.030 | 0.959 | 48.98 | -26.62 |
| 5 | M15 | 100 | 3.0 | 1.5 | 2.0 | newyork | 0.854 | 0.956 | 74.10 | -48.17 |
| 6 | M15 | 20 | 3.0 | 1.5 | 3.0 | newyork | 0.881 | 0.954 | 53.27 | -25.78 |
| 7 | M15 | 100 | 3.0 | 1.5 | 3.0 | newyork | 0.828 | 0.953 | 77.09 | -56.70 |
| 8 | M15 | 100 | 2.0 | 1.5 | 4.0 | asian | 1.028 | 0.952 | 83.65 | -67.66 |
| 9 | M15 | 20 | 3.0 | 1.0 | 4.0 | newyork | 0.609 | 0.950 | 45.80 | -30.63 |
| 10 | M15 | 20 | 2.0 | 1.5 | 4.0 | london | 0.862 | 0.941 | 92.22 | -87.71 |
