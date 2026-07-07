# ATR Channel Breakout — EURUSD M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]

- Generated: 2026-07-07 18:21:17 UTC  |  Combinations: 288
- Train: 2020  |  OOS: 2021-2025

## Logic
- Channel: EMA(ema_period) ± atr_channel_mult × ATR(14)
- Long:  prev_close ≤ upper  AND  close > upper
- Short: prev_close ≥ lower  AND  close < lower
- Entry: next-bar open  |  SL: ±sl_mult×ATR  |  TP: SL×rr
- Session filter on signal bar

## Best Setup
- TF=M1  EMA=100  ATR_mult=1.5
- SL_mult=1.5  RR=4.0  Session=london
- Train PF=0.8229  |  OOS PF=0.8152
- OOS DD=100.00%  |  OOS P&L=-100.00%

## Top 10

| # | TF | EMA | ATR | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 100 | 1.5 | 1.5 | 4.0 | london | 0.823 | 0.815 | 100.00 | -100.00 |
| 2 | M1 | 50 | 1.5 | 1.5 | 4.0 | london | 0.884 | 0.814 | 100.00 | -100.00 |
| 3 | M1 | 100 | 2.0 | 1.5 | 4.0 | london | 0.848 | 0.814 | 100.00 | -100.00 |
| 4 | M1 | 100 | 2.0 | 1.5 | 3.0 | london | 0.837 | 0.808 | 100.00 | -100.00 |
| 5 | M1 | 100 | 2.5 | 1.5 | 4.0 | london | 0.829 | 0.805 | 100.00 | -100.00 |
| 6 | M1 | 50 | 1.5 | 1.5 | 3.0 | london | 0.853 | 0.805 | 100.00 | -100.00 |
| 7 | M1 | 100 | 1.5 | 1.5 | 3.0 | london | 0.803 | 0.804 | 100.00 | -100.00 |
| 8 | M1 | 50 | 2.0 | 1.5 | 4.0 | london | 0.852 | 0.801 | 100.00 | -100.00 |
| 9 | M1 | 100 | 3.0 | 1.5 | 4.0 | london | 0.860 | 0.799 | 100.00 | -100.00 |
| 10 | M1 | 100 | 2.5 | 1.5 | 3.0 | london | 0.804 | 0.799 | 100.00 | -100.00 |
