# Fractal + FFT Confluence (#18) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

- Generated: 2026-07-07 18:23:56 UTC  |  Combos totali: 432
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#05 Fractal S/R**: pivot Williams → livelli attivi nella finestra lookback
- **#11 FFT Cycle**: slope del ciclo dominante concorda con il bounce
- **#12 FFT Regime**: regime CYCLE come gate opzionale (full_confl)
- LONG = bounce da supporto AND slope>0 AND [regime=CYCLE]

## Best Full Confluence (≥100 trade OOS)
- TF=M1  fp=5  tol=0.5  lb=30
- N=64  delta=0.03  min_p=10
- RR=3.0  Session=london
- Train PF=0.8442 | OOS PF=0.8116
- OOS DD=100.00%  OOS Trades=8985
- PF Gain=+0.008  DD Gain=+0.000

## Top 15 Full Confl

| # | TF | fp | tol | lb | N | δ | Sess | RR | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 5 | 0.5 | 30 | 64 | 0.03 | london | 3.0 | 0.844 | 0.812 | 100.0 | 8985 | +0.008 |
| 2 | M1 | 5 | 0.5 | 30 | 64 | 0.05 | london | 3.0 | 0.839 | 0.811 | 100.0 | 8506 | +0.008 |
| 3 | M1 | 5 | 0.5 | 30 | 64 | 0.03 | london | 3.0 | 0.838 | 0.809 | 100.0 | 20379 | +0.006 |
| 4 | M1 | 5 | 0.5 | 30 | 64 | 0.05 | london | 3.0 | 0.847 | 0.809 | 100.0 | 19406 | +0.005 |
| 5 | M1 | 5 | 1.0 | 70 | 64 | 0.03 | london | 3.0 | 0.834 | 0.806 | 100.0 | 63002 | -0.003 |
| 6 | M1 | 5 | 0.3 | 30 | 64 | 0.05 | london | 3.0 | 0.850 | 0.806 | 100.0 | 5254 | +0.001 |
| 7 | M1 | 5 | 1.0 | 70 | 64 | 0.05 | london | 3.0 | 0.833 | 0.805 | 100.0 | 60023 | -0.003 |
| 8 | M1 | 5 | 0.3 | 30 | 64 | 0.05 | london | 3.0 | 0.850 | 0.805 | 100.0 | 11963 | +0.001 |
| 9 | M1 | 5 | 0.3 | 30 | 64 | 0.03 | london | 3.0 | 0.859 | 0.804 | 100.0 | 5560 | -0.000 |
| 10 | M1 | 5 | 0.5 | 70 | 64 | 0.03 | london | 3.0 | 0.829 | 0.804 | 100.0 | 34689 | -0.004 |
| 11 | M1 | 5 | 0.3 | 70 | 64 | 0.05 | london | 3.0 | 0.835 | 0.803 | 100.0 | 21276 | -0.008 |
| 12 | M1 | 5 | 0.5 | 70 | 64 | 0.05 | london | 3.0 | 0.833 | 0.803 | 100.0 | 33021 | -0.005 |
| 13 | M1 | 5 | 0.3 | 70 | 64 | 0.03 | london | 3.0 | 0.835 | 0.803 | 100.0 | 22376 | -0.009 |
| 14 | M1 | 5 | 0.3 | 30 | 64 | 0.03 | london | 3.0 | 0.846 | 0.803 | 100.0 | 12581 | -0.002 |
| 15 | M1 | 5 | 1.0 | 30 | 64 | 0.03 | london | 3.0 | 0.833 | 0.802 | 100.0 | 40520 | -0.004 |
