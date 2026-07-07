# EMA Ribbon Direction Filter — EURUSD M15

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-07-07 18:21:19 UTC  |  Combinations: 288
- Train: 2020  |  OOS: 2021-2025

## Logic
- Ribbon: EMA(fast) / EMA(mid) / EMA(slow)  — condizione: fast < mid < slow
- Long:  ribbon JUST turned fully bullish  (fast>mid>slow, bar prec. NO)
- Short: ribbon JUST turned fully bearish  (fast<mid<slow, bar prec. NO)
- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M15  fast=13  mid=34  slow=55
- SL_mult=1.5  RR=4.0  Session=newyork
- Train PF=1.0080  |  OOS PF=0.9994
- OOS DD=38.78%  |  OOS P&L=-16.92%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 13 | 34 | 55 | 1.5 | 4.0 | newyork | 1.008 | 0.999 | 38.78 | -16.92 |
| 2 | M15 | 8 | 34 | 55 | 1.5 | 4.0 | newyork | 1.028 | 0.989 | 49.33 | -25.94 |
| 3 | M15 | 8 | 21 | 55 | 1.0 | 4.0 | london | 1.003 | 0.985 | 80.11 | -47.49 |
| 4 | M15 | 5 | 34 | 55 | 1.5 | 4.0 | london | 1.267 | 0.980 | 57.24 | -48.51 |
| 5 | M15 | 8 | 21 | 89 | 1.0 | 4.0 | london | 1.125 | 0.979 | 82.85 | -50.87 |
| 6 | M15 | 8 | 21 | 55 | 1.5 | 4.0 | london | 1.106 | 0.976 | 69.98 | -53.83 |
| 7 | M15 | 13 | 34 | 55 | 1.0 | 4.0 | london | 1.112 | 0.965 | 60.25 | -49.58 |
| 8 | M15 | 8 | 21 | 55 | 1.0 | 3.0 | london | 0.931 | 0.960 | 77.64 | -59.68 |
| 9 | M15 | 13 | 21 | 89 | 1.5 | 4.0 | newyork | 0.998 | 0.960 | 50.94 | -42.54 |
| 10 | M15 | 5 | 34 | 55 | 1.5 | 3.0 | london | 1.230 | 0.960 | 68.96 | -57.18 |
