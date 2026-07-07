# EMA Ribbon Direction Filter — EURUSD M5

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
| 4 | M5 | 13 | 34 | 55 | 1.0 | 4.0 | asian | 0.988 | 1.103 | 57.56 | 493.31 |
| 5 | M5 | 5 | 34 | 55 | 1.5 | 4.0 | asian | 1.022 | 1.094 | 62.32 | 826.21 |
| 6 | M5 | 8 | 34 | 55 | 1.5 | 4.0 | asian | 0.971 | 1.090 | 52.24 | 475.97 |
| 7 | M5 | 5 | 34 | 55 | 1.0 | 4.0 | asian | 1.044 | 1.088 | 60.04 | 660.53 |
| 8 | M5 | 8 | 34 | 89 | 1.0 | 4.0 | asian | 1.000 | 1.087 | 62.85 | 393.55 |
| 9 | M5 | 5 | 34 | 89 | 1.0 | 4.0 | asian | 1.046 | 1.084 | 56.26 | 539.36 |
| 10 | M5 | 13 | 34 | 55 | 1.0 | 2.0 | asian | 1.097 | 1.083 | 36.39 | 269.16 |
