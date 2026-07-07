# ATR Channel Breakout — EURUSD ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-05-08 07:44:47 UTC  |  Combinations: 864
- Train: 2020-2023  |  OOS: 2024-2025

## Logic
- Channel: EMA(ema_period) ± atr_channel_mult × ATR(14)
- Long:  prev_close ≤ upper  AND  close > upper
- Short: prev_close ≥ lower  AND  close < lower
- Entry: next-bar open  |  SL: ±sl_mult×ATR  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M15  EMA=20  ATR_mult=2.5
- SL_mult=1.5  RR=4.0  Session=asian
- Train PF=0.7910  |  OOS PF=1.0938
- OOS DD=64.14%  |  OOS P&L=112.81%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 20 | 2.5 | 1.5 | 4.0 | asian | 0.791 | 1.094 | 64.14 | 112.81 |
| 2 | M1 | 100 | 2.5 | 1.0 | 3.0 | asian | 1.008 | 1.062 | 87.37 | 1705996.39 |
| 3 | M15 | 100 | 2.0 | 1.0 | 4.0 | asian | 0.997 | 1.057 | 77.78 | 80.62 |
| 4 | M1 | 100 | 2.0 | 1.0 | 4.0 | asian | 1.078 | 1.054 | 98.33 | 281516.52 |
| 5 | M1 | 100 | 3.0 | 1.0 | 3.0 | asian | 0.997 | 1.054 | 82.88 | 111980.15 |
| 6 | M1 | 100 | 2.5 | 1.0 | 4.0 | asian | 1.040 | 1.052 | 98.97 | 80064.62 |
| 7 | M1 | 50 | 2.0 | 1.0 | 4.0 | london | 0.988 | 1.050 | 99.78 | 313077.93 |
| 8 | M1 | 50 | 1.5 | 1.0 | 3.0 | asian | 1.056 | 1.049 | 98.59 | 2221336.39 |
| 9 | M1 | 100 | 1.5 | 1.0 | 3.0 | london | 1.039 | 1.049 | 96.60 | 254262.40 |
| 10 | M1 | 50 | 2.0 | 1.0 | 3.0 | london | 0.993 | 1.049 | 98.17 | 693079.03 |
