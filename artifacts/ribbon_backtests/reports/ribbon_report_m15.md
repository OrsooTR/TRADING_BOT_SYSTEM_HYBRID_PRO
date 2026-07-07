# EMA Ribbon Direction Filter — EURUSD M15

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
- TF=M15  fast=13  mid=21  slow=89
- SL_mult=1.0  RR=3.0  Session=asian
- Train PF=1.1466  |  OOS PF=1.1041
- OOS DD=30.81%  |  OOS P&L=119.84%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 13 | 21 | 89 | 1.0 | 3.0 | asian | 1.147 | 1.104 | 30.81 | 119.84 |
| 2 | M15 | 13 | 34 | 55 | 1.0 | 2.0 | asian | 1.083 | 1.101 | 33.27 | 85.09 |
| 3 | M15 | 13 | 21 | 89 | 1.0 | 4.0 | asian | 1.177 | 1.092 | 48.35 | 95.65 |
| 4 | M15 | 5 | 34 | 55 | 1.0 | 3.0 | asian | 1.151 | 1.091 | 33.66 | 120.60 |
| 5 | M15 | 5 | 21 | 89 | 1.0 | 2.0 | asian | 1.177 | 1.088 | 32.32 | 130.82 |
| 6 | M15 | 5 | 34 | 55 | 1.0 | 2.0 | asian | 1.156 | 1.087 | 29.33 | 103.86 |
| 7 | M15 | 8 | 21 | 55 | 1.5 | 4.0 | asian | 1.048 | 1.086 | 50.00 | 117.61 |
| 8 | M15 | 8 | 21 | 89 | 1.0 | 2.0 | asian | 1.085 | 1.079 | 41.24 | 88.50 |
| 9 | M15 | 13 | 21 | 89 | 1.0 | 2.0 | asian | 1.181 | 1.079 | 39.86 | 71.17 |
| 10 | M15 | 5 | 34 | 55 | 1.5 | 4.0 | asian | 1.202 | 1.076 | 37.02 | 82.94 |
