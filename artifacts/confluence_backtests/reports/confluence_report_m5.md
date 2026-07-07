# FFT + Derivative Confluence (#17) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_derivative_confluence]]

- Generated: 2026-07-07 18:26:05 UTC  |  Combos: 5232
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#12 FFT Regime**: CYCLE quando mid_ratio > hf_ratio + delta
- **#11 FFT Cycle**: slope del ciclo dominante (direzione)
- **#02 Derivata**: d1 zero-crossing (trigger di entrata)
- LONG = d1↑ AND slope>0 AND CYCLE_regime
- SHORT = d1↓ AND slope<0 AND CYCLE_regime
- Entry: next-bar open | SL: sl_mult×ATR(14) | TP: SL×rr

## Best Full Confluence Setup
- TF=M5  N=128  delta=0.05
- min_period=5b  pwr_thresh=0.12
- ema_period=10  sl=1.5  rr=4.0
- Session=london
- Train PF=inf | OOS PF=1.6414
- OOS DD=7.34%  |  OOS P&L=25.85%
- Trades=51  Reduction=99.9%
- PF Gain vs baseline=+0.715  DD Gain=+92.660

## Top 15 Full Confluence

| # | TF | N | δ | minP | pwrT | EMA | SL | RR | Sess | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.5 | 4.0 | london | inf | 1.641 | 7.3 | 51 | +0.715 |
| 2 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.5 | 4.0 | london | inf | 1.641 | 7.3 | 51 | +0.715 |
| 3 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.5 | 4.0 | newyork | 3.683 | 1.573 | 8.3 | 33 | +0.696 |
| 4 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.5 | 4.0 | newyork | 3.683 | 1.573 | 8.3 | 33 | +0.696 |
| 5 | M5 | 128 | 0.03 | 5 | 0.12 | 10 | 1.5 | 4.0 | london | inf | 1.553 | 7.3 | 53 | +0.627 |
| 6 | M5 | 128 | 0.08 | 3 | 0.12 | 10 | 1.5 | 4.0 | london | 0.404 | 1.550 | 14.5 | 77 | +0.624 |
| 7 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.5 | 3.0 | newyork | 2.745 | 1.538 | 8.6 | 33 | +0.655 |
| 8 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.5 | 3.0 | newyork | 2.745 | 1.538 | 8.6 | 33 | +0.655 |
| 9 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.0 | 4.0 | newyork | 3.539 | 1.497 | 8.1 | 33 | +0.651 |
| 10 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.0 | 4.0 | newyork | 3.539 | 1.497 | 8.1 | 33 | +0.651 |
| 11 | M5 | 128 | 0.05 | 3 | 0.12 | 10 | 1.0 | 4.0 | newyork | 3.539 | 1.473 | 14.6 | 57 | +0.627 |
| 12 | M5 | 128 | 0.08 | 3 | 0.12 | 10 | 1.0 | 4.0 | newyork | 3.539 | 1.473 | 14.6 | 57 | +0.627 |
| 13 | M5 | 128 | 0.05 | 3 | 0.12 | 10 | 1.5 | 4.0 | london | 0.404 | 1.468 | 16.7 | 80 | +0.542 |
| 14 | M5 | 128 | 0.05 | 5 | 0.12 | 10 | 1.5 | 3.0 | london | inf | 1.457 | 7.3 | 51 | +0.542 |
| 15 | M5 | 128 | 0.08 | 5 | 0.12 | 10 | 1.5 | 3.0 | london | inf | 1.457 | 7.3 | 51 | +0.542 |
