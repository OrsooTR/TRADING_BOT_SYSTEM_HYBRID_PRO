# FFT + Derivative Confluence (#17) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_derivative_confluence]]

- Generated: 2026-05-11 08:41:02 UTC  |  Combos: 10464
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#12 FFT Regime**: CYCLE quando mid_ratio > hf_ratio + delta
- **#11 FFT Cycle**: slope del ciclo dominante (direzione)
- **#02 Derivata**: d1 zero-crossing (trigger di entrata)
- LONG = d1↑ AND slope>0 AND CYCLE_regime
- SHORT = d1↓ AND slope<0 AND CYCLE_regime
- Entry: next-bar open | SL: sl_mult×ATR(14) | TP: SL×rr

## Best Full Confluence Setup
- TF=M15  N=128  delta=0.05
- min_period=10b  pwr_thresh=0.08
- ema_period=20  sl=1.0  rr=2.0
- Session=london
- Train PF=0.0000 | OOS PF=2.0833
- OOS DD=5.88%  |  OOS P&L=28.90%
- Trades=49  Reduction=99.6%
- PF Gain vs baseline=+1.102  DD Gain=+82.260

## Top 15 Full Confluence

| # | TF | N | δ | minP | pwrT | EMA | SL | RR | Sess | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 2.0 | london | 0.000 | 2.083 | 5.9 | 49 | +1.102 |
| 2 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 2.0 | london | 0.000 | 2.083 | 5.9 | 49 | +1.102 |
| 3 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 2.0 | london | 0.000 | 2.080 | 5.9 | 51 | +1.098 |
| 4 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 3.0 | london | 0.000 | 2.069 | 5.0 | 49 | +1.104 |
| 5 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 3.0 | london | 0.000 | 2.069 | 5.0 | 49 | +1.104 |
| 6 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 3.0 | london | 0.000 | 1.935 | 5.0 | 51 | +0.970 |
| 7 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 4.0 | london | 0.000 | 1.818 | 7.7 | 49 | +0.871 |
| 8 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 4.0 | london | 0.000 | 1.818 | 7.7 | 49 | +0.871 |
| 9 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.5 | 2.0 | london | 0.000 | 1.769 | 5.9 | 49 | +0.816 |
| 10 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.5 | 2.0 | london | 0.000 | 1.769 | 5.9 | 49 | +0.816 |
| 11 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 4.0 | london | 0.000 | 1.714 | 8.7 | 51 | +0.767 |
| 12 | M15 | 128 | 0.03 | 10 | 0.08 | 10 | 1.0 | 2.0 | london | 1.333 | 1.707 | 7.8 | 76 | +0.712 |
| 13 | M5 | 128 | 0.08 | 3 | 0.12 | 10 | 1.5 | 4.0 | asian | 0.667 | 1.684 | 15.0 | 81 | +0.662 |
| 14 | M15 | 128 | 0.05 | 10 | 0.08 | 10 | 1.0 | 2.0 | london | 1.333 | 1.659 | 7.8 | 75 | +0.663 |
| 15 | M15 | 128 | 0.08 | 10 | 0.08 | 10 | 1.0 | 2.0 | london | 1.333 | 1.659 | 7.8 | 75 | +0.663 |
