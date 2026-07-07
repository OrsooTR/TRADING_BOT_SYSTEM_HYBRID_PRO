# EMA Ribbon Direction Filter — EURUSD M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-05-08 07:46:34 UTC  |  Combinations: 288
- Train: 2020-2023  |  OOS: 2024-2025

## Logic
- Ribbon: EMA(fast) / EMA(mid) / EMA(slow)  — condizione: fast < mid < slow
- Long:  ribbon JUST turned fully bullish  (fast>mid>slow, bar prec. NO)
- Short: ribbon JUST turned fully bearish  (fast<mid<slow, bar prec. NO)
- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M1  fast=5  mid=21  slow=89
- SL_mult=1.0  RR=4.0  Session=asian
- Train PF=1.0900  |  OOS PF=1.0745
- OOS DD=79.77%  |  OOS P&L=1008627.77%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 5 | 21 | 89 | 1.0 | 4.0 | asian | 1.090 | 1.075 | 79.77 | 1008627.77 |
| 2 | M1 | 8 | 21 | 89 | 1.0 | 4.0 | asian | 1.086 | 1.074 | 78.99 | 222921.35 |
| 3 | M1 | 5 | 21 | 55 | 1.0 | 4.0 | asian | 1.065 | 1.071 | 84.68 | 830605.96 |
| 4 | M1 | 8 | 21 | 55 | 1.0 | 4.0 | asian | 1.069 | 1.069 | 80.76 | 149347.38 |
| 5 | M1 | 5 | 21 | 55 | 1.0 | 3.0 | asian | 1.032 | 1.069 | 77.13 | 794688.90 |
| 6 | M1 | 13 | 21 | 55 | 1.0 | 4.0 | asian | 1.081 | 1.067 | 73.32 | 35654.89 |
| 7 | M1 | 13 | 34 | 89 | 1.0 | 4.0 | asian | 1.095 | 1.064 | 70.53 | 5959.12 |
| 8 | M1 | 13 | 21 | 55 | 1.0 | 3.0 | asian | 1.041 | 1.064 | 68.38 | 34168.47 |
| 9 | M1 | 5 | 21 | 89 | 1.0 | 3.0 | asian | 1.056 | 1.063 | 77.52 | 179330.06 |
| 10 | M1 | 13 | 21 | 89 | 1.0 | 4.0 | asian | 1.087 | 1.063 | 85.79 | 14279.62 |
