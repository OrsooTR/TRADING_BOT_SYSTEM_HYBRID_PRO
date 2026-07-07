# ATR Channel Breakout — EURUSD M5

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
- TF=M5  EMA=50  ATR_mult=3.0
- SL_mult=1.5  RR=4.0  Session=london
- Train PF=0.9297  |  OOS PF=0.9411
- OOS DD=99.02%  |  OOS P&L=-98.10%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 50 | 3.0 | 1.5 | 4.0 | london | 0.930 | 0.941 | 99.02 | -98.10 |
| 2 | M5 | 100 | 3.0 | 1.5 | 4.0 | london | 0.853 | 0.897 | 99.94 | -99.91 |
| 3 | M5 | 20 | 3.0 | 1.5 | 4.0 | newyork | 0.873 | 0.896 | 85.15 | -79.03 |
| 4 | M5 | 50 | 1.5 | 1.5 | 4.0 | london | 0.888 | 0.896 | 100.00 | -100.00 |
| 5 | M5 | 50 | 2.0 | 1.5 | 4.0 | london | 0.909 | 0.894 | 100.00 | -100.00 |
| 6 | M5 | 50 | 2.5 | 1.5 | 4.0 | london | 0.888 | 0.893 | 99.98 | -99.97 |
| 7 | M5 | 100 | 2.5 | 1.5 | 4.0 | london | 0.919 | 0.893 | 99.98 | -99.97 |
| 8 | M5 | 50 | 3.0 | 1.5 | 3.0 | london | 0.932 | 0.891 | 99.81 | -99.70 |
| 9 | M5 | 100 | 1.5 | 1.5 | 4.0 | london | 0.963 | 0.886 | 100.00 | -100.00 |
| 10 | M5 | 100 | 1.5 | 1.5 | 3.0 | london | 0.925 | 0.886 | 99.99 | -99.99 |
