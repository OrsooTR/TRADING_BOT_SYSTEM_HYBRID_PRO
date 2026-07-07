# ATR Channel Breakout — EURUSD M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-05-08 07:44:47 UTC  |  Combinations: 288
- Train: 2020-2023  |  OOS: 2024-2025

## Logic
- Channel: EMA(ema_period) ± atr_channel_mult × ATR(14)
- Long:  prev_close ≤ upper  AND  close > upper
- Short: prev_close ≥ lower  AND  close < lower
- Entry: next-bar open  |  SL: ±sl_mult×ATR  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M1  EMA=100  ATR_mult=2.5
- SL_mult=1.0  RR=3.0  Session=asian
- Train PF=1.0081  |  OOS PF=1.0620
- OOS DD=87.37%  |  OOS P&L=1705996.39%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 100 | 2.5 | 1.0 | 3.0 | asian | 1.008 | 1.062 | 87.37 | 1705996.39 |
| 2 | M1 | 100 | 2.0 | 1.0 | 4.0 | asian | 1.078 | 1.054 | 98.33 | 281516.52 |
| 3 | M1 | 100 | 3.0 | 1.0 | 3.0 | asian | 0.997 | 1.054 | 82.88 | 111980.15 |
| 4 | M1 | 100 | 2.5 | 1.0 | 4.0 | asian | 1.040 | 1.052 | 98.97 | 80064.62 |
| 5 | M1 | 50 | 2.0 | 1.0 | 4.0 | london | 0.988 | 1.050 | 99.78 | 313077.93 |
| 6 | M1 | 50 | 1.5 | 1.0 | 3.0 | asian | 1.056 | 1.049 | 98.59 | 2221336.39 |
| 7 | M1 | 100 | 1.5 | 1.0 | 3.0 | london | 1.039 | 1.049 | 96.60 | 254262.40 |
| 8 | M1 | 50 | 2.0 | 1.0 | 3.0 | london | 0.993 | 1.049 | 98.17 | 693079.03 |
| 9 | M1 | 100 | 2.0 | 1.0 | 4.0 | london | 1.006 | 1.048 | 96.54 | 58643.85 |
| 10 | M1 | 100 | 1.5 | 1.0 | 4.0 | asian | 1.007 | 1.048 | 99.42 | 80074.81 |
