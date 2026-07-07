# EMA Ribbon Direction Filter — EURUSD ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-05-08 07:46:34 UTC  |  Combinations: 864
- Train: 2020-2023  |  OOS: 2024-2025

## Logic
- Ribbon: EMA(fast) / EMA(mid) / EMA(slow)  — condizione: fast < mid < slow
- Long:  ribbon JUST turned fully bullish  (fast>mid>slow, bar prec. NO)
- Short: ribbon JUST turned fully bearish  (fast<mid<slow, bar prec. NO)
- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M5  fast=13  mid=34  slow=55
- SL_mult=1.5  RR=4.0  Session=asian
- Train PF=0.9780  |  OOS PF=1.1269
- OOS DD=52.84%  |  OOS P&L=920.15%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 13 | 34 | 55 | 1.5 | 4.0 | asian | 0.978 | 1.127 | 52.84 | 920.15 |
| 2 | M5 | 8 | 34 | 55 | 1.0 | 4.0 | asian | 1.014 | 1.111 | 58.41 | 890.33 |
| 3 | M5 | 13 | 34 | 55 | 1.5 | 3.0 | asian | 0.964 | 1.109 | 43.41 | 565.75 |
| 4 | M15 | 13 | 21 | 89 | 1.0 | 3.0 | asian | 1.147 | 1.104 | 30.81 | 119.84 |
| 5 | M5 | 13 | 34 | 55 | 1.0 | 4.0 | asian | 0.988 | 1.103 | 57.56 | 493.31 |
| 6 | M15 | 13 | 34 | 55 | 1.0 | 2.0 | asian | 1.083 | 1.101 | 33.27 | 85.09 |
| 7 | M5 | 5 | 34 | 55 | 1.5 | 4.0 | asian | 1.022 | 1.094 | 62.32 | 826.21 |
| 8 | M15 | 13 | 21 | 89 | 1.0 | 4.0 | asian | 1.177 | 1.092 | 48.35 | 95.65 |
| 9 | M15 | 5 | 34 | 55 | 1.0 | 3.0 | asian | 1.151 | 1.091 | 33.66 | 120.60 |
| 10 | M5 | 8 | 34 | 55 | 1.5 | 4.0 | asian | 0.971 | 1.090 | 52.24 | 475.97 |
