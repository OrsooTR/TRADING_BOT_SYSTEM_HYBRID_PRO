# FFT + Derivative Confluence (#17) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_derivative_confluence]]

- Generated: 2026-05-11 08:41:02 UTC  |  Combos: 5232
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#12 FFT Regime**: CYCLE quando mid_ratio > hf_ratio + delta
- **#11 FFT Cycle**: slope del ciclo dominante (direzione)
- **#02 Derivata**: d1 zero-crossing (trigger di entrata)
- LONG = d1↑ AND slope>0 AND CYCLE_regime
- SHORT = d1↓ AND slope<0 AND CYCLE_regime
- Entry: next-bar open | SL: sl_mult×ATR(14) | TP: SL×rr

## Best Full Confluence Setup
- TF=M5  N=128  delta=0.08
- min_period=3b  pwr_thresh=0.12
- ema_period=10  sl=1.5  rr=4.0
- Session=asian
- Train PF=0.6667 | OOS PF=1.6842
- OOS DD=15.02%  |  OOS P&L=44.55%
- Trades=81  Reduction=99.9%
- PF Gain vs baseline=+0.662  DD Gain=+82.930

## Top 15 Full Confluence

| # | TF | N | δ | minP | pwrT | EMA | SL | RR | Sess | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 128 | 0.08 | 3 | 0.12 | 10 | 1.5 | 4.0 | asian | 0.667 | 1.684 | 15.0 | 81 | +0.662 |
| 2 | M5 | 128 | 0.03 | 5 | 0.12 | 10 | 1.0 | 2.0 | asian | 2.000 | 1.636 | 5.0 | 60 | +0.607 |
| 3 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.0 | 2.0 | asian | 2.000 | 1.636 | 5.0 | 60 | +0.607 |
| 4 | M5 | 128 | 0.08 | 10 | 0.12 | 10 | 1.5 | 4.0 | all | 0.000 | 1.636 | 10.5 | 31 | +0.676 |
| 5 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.0 | 4.0 | london | 4.000 | 1.630 | 9.7 | 38 | +0.636 |
| 6 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.0 | 4.0 | london | 4.000 | 1.630 | 9.7 | 38 | +0.636 |
| 7 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.5 | 4.0 | london | 4.000 | 1.630 | 9.7 | 38 | +0.663 |
| 8 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.5 | 4.0 | london | 4.000 | 1.630 | 9.7 | 38 | +0.663 |
| 9 | M5 | 128 | 0.03 | 3 | 0.12 | 10 | 1.0 | 2.0 | asian | 1.111 | 1.617 | 5.8 | 85 | +0.588 |
| 10 | M5 | 128 | 0.05 | 3 | 0.12 | 10 | 1.0 | 2.0 | asian | 1.111 | 1.617 | 5.8 | 85 | +0.588 |
| 11 | M5 | 128 | 0.03 | 5 | 0.12 | 10 | 1.0 | 3.0 | asian | 3.000 | 1.615 | 10.5 | 60 | +0.578 |
| 12 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.0 | 3.0 | asian | 3.000 | 1.615 | 10.5 | 60 | +0.578 |
| 13 | M5 | 128 | 0.08 | 3 | 0.12 | 10 | 1.0 | 2.0 | asian | 1.111 | 1.600 | 5.8 | 81 | +0.571 |
| 14 | M5 | 128 | 0.03 | 10 | 0.12 | 10 | 1.5 | 4.0 | all | 0.000 | 1.600 | 12.2 | 35 | +0.639 |
| 15 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.0 | 2.0 | asian | 2.000 | 1.576 | 5.0 | 59 | +0.546 |
