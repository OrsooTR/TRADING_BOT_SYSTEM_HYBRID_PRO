# EMA Ribbon Direction Filter — EURUSD ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-07-07 18:21:19 UTC  |  Combinations: 864
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
| 2 | M5 | 13 | 34 | 55 | 1.5 | 4.0 | london | 1.023 | 0.994 | 72.32 | -58.78 |
| 3 | M15 | 8 | 34 | 55 | 1.5 | 4.0 | newyork | 1.028 | 0.989 | 49.33 | -25.94 |
| 4 | M15 | 8 | 21 | 55 | 1.0 | 4.0 | london | 1.003 | 0.985 | 80.11 | -47.49 |
| 5 | M5 | 5 | 34 | 55 | 1.5 | 4.0 | london | 1.064 | 0.981 | 88.35 | -82.47 |
| 6 | M15 | 5 | 34 | 55 | 1.5 | 4.0 | london | 1.267 | 0.980 | 57.24 | -48.51 |
| 7 | M5 | 8 | 34 | 55 | 1.5 | 4.0 | london | 1.058 | 0.980 | 84.46 | -77.88 |
| 8 | M15 | 8 | 21 | 89 | 1.0 | 4.0 | london | 1.125 | 0.979 | 82.85 | -50.87 |
| 9 | M15 | 8 | 21 | 55 | 1.5 | 4.0 | london | 1.106 | 0.976 | 69.98 | -53.83 |
| 10 | M5 | 13 | 21 | 89 | 1.5 | 4.0 | london | 1.018 | 0.969 | 91.19 | -85.10 |
