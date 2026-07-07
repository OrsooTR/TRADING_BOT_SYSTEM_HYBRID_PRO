# EMA Ribbon Direction Filter — EURUSD M5

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
- TF=M5  fast=13  mid=34  slow=55
- SL_mult=1.5  RR=4.0  Session=london
- Train PF=1.0226  |  OOS PF=0.9940
- OOS DD=72.32%  |  OOS P&L=-58.78%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 13 | 34 | 55 | 1.5 | 4.0 | london | 1.023 | 0.994 | 72.32 | -58.78 |
| 2 | M5 | 5 | 34 | 55 | 1.5 | 4.0 | london | 1.064 | 0.981 | 88.35 | -82.47 |
| 3 | M5 | 8 | 34 | 55 | 1.5 | 4.0 | london | 1.058 | 0.980 | 84.46 | -77.88 |
| 4 | M5 | 13 | 21 | 89 | 1.5 | 4.0 | london | 1.018 | 0.969 | 91.19 | -85.10 |
| 5 | M5 | 13 | 21 | 55 | 1.5 | 4.0 | london | 1.019 | 0.967 | 93.38 | -87.67 |
| 6 | M5 | 13 | 34 | 55 | 1.5 | 3.0 | london | 0.957 | 0.965 | 83.77 | -77.60 |
| 7 | M5 | 13 | 21 | 89 | 1.5 | 3.0 | london | 0.980 | 0.962 | 89.23 | -83.98 |
| 8 | M5 | 5 | 34 | 55 | 1.5 | 3.0 | london | 1.009 | 0.953 | 93.50 | -91.88 |
| 9 | M5 | 5 | 34 | 89 | 1.5 | 4.0 | london | 1.094 | 0.951 | 95.98 | -94.27 |
| 10 | M5 | 8 | 34 | 55 | 1.5 | 3.0 | london | 1.001 | 0.949 | 91.78 | -89.45 |
