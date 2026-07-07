# FFT + Derivative Confluence (#17) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_derivative_confluence]]

- Generated: 2026-07-07 18:26:05 UTC  |  Combos: 10464
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
- ema_period=20  sl=1.0  rr=3.0
- Session=newyork
- Train PF=0.0000 | OOS PF=2.1933
- OOS DD=5.24%  |  OOS P&L=36.29%
- Trades=45  Reduction=99.6%
- PF Gain vs baseline=+1.318  DD Gain=+94.510

## Top 15 Full Confluence

| # | TF | N | δ | minP | pwrT | EMA | SL | RR | Sess | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 3.0 | newyork | 0.000 | 2.193 | 5.2 | 45 | +1.318 |
| 2 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 3.0 | newyork | 0.000 | 2.193 | 5.2 | 45 | +1.318 |
| 3 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 2.0 | newyork | 0.000 | 2.063 | 5.5 | 45 | +1.184 |
| 4 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 2.0 | newyork | 0.000 | 2.063 | 5.5 | 45 | +1.184 |
| 5 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 2.0 | newyork | 0.000 | 2.053 | 5.5 | 47 | +1.174 |
| 6 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.5 | 4.0 | newyork | 0.000 | 2.034 | 6.0 | 45 | +1.165 |
| 7 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.5 | 4.0 | newyork | 0.000 | 2.034 | 6.0 | 45 | +1.165 |
| 8 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 3.0 | newyork | 0.000 | 2.032 | 5.2 | 47 | +1.157 |
| 9 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.5 | 2.0 | newyork | 0.000 | 1.953 | 5.3 | 45 | +1.066 |
| 10 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.5 | 2.0 | newyork | 0.000 | 1.953 | 5.3 | 45 | +1.066 |
| 11 | M15 | 128 | 0.05 | 10 | 0.08 | 20 | 1.0 | 4.0 | newyork | 0.000 | 1.952 | 7.4 | 45 | +1.095 |
| 12 | M15 | 128 | 0.08 | 10 | 0.08 | 20 | 1.0 | 4.0 | newyork | 0.000 | 1.952 | 7.4 | 45 | +1.095 |
| 13 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.5 | 4.0 | newyork | 0.000 | 1.899 | 7.0 | 47 | +1.031 |
| 14 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 4.0 | newyork | 0.000 | 1.828 | 8.3 | 47 | +0.970 |
| 15 | M15 | 128 | 0.03 | 10 | 0.08 | 20 | 1.0 | 2.0 | london | 0.876 | 1.791 | 4.6 | 46 | +0.901 |
