# EMA Ribbon Direction Filter — EURUSD M1

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
- TF=M1  fast=5  mid=34  slow=55
- SL_mult=1.5  RR=4.0  Session=london
- Train PF=0.8657  |  OOS PF=0.8361
- OOS DD=100.00%  |  OOS P&L=-100.00%

## Top 10

| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 5 | 34 | 55 | 1.5 | 4.0 | london | 0.866 | 0.836 | 100.00 | -100.00 |
| 2 | M1 | 8 | 34 | 55 | 1.5 | 4.0 | london | 0.866 | 0.836 | 100.00 | -100.00 |
| 3 | M1 | 13 | 21 | 55 | 1.5 | 4.0 | london | 0.845 | 0.831 | 100.00 | -100.00 |
| 4 | M1 | 13 | 34 | 55 | 1.5 | 4.0 | london | 0.865 | 0.831 | 100.00 | -100.00 |
| 5 | M1 | 5 | 21 | 55 | 1.5 | 4.0 | london | 0.854 | 0.829 | 100.00 | -100.00 |
| 6 | M1 | 5 | 21 | 89 | 1.5 | 4.0 | london | 0.864 | 0.822 | 100.00 | -100.00 |
| 7 | M1 | 5 | 34 | 89 | 1.5 | 4.0 | london | 0.823 | 0.822 | 100.00 | -100.00 |
| 8 | M1 | 8 | 34 | 89 | 1.5 | 4.0 | london | 0.806 | 0.821 | 100.00 | -100.00 |
| 9 | M1 | 8 | 21 | 55 | 1.5 | 4.0 | london | 0.834 | 0.820 | 100.00 | -100.00 |
| 10 | M1 | 5 | 34 | 55 | 1.5 | 3.0 | london | 0.827 | 0.820 | 100.00 | -100.00 |
