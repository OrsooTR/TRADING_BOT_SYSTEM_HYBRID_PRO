# Fractal + FFT Confluence (#18) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

- Generated: 2026-07-07 18:23:56 UTC  |  Combos totali: 816
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#05 Fractal S/R**: pivot Williams → livelli attivi nella finestra lookback
- **#11 FFT Cycle**: slope del ciclo dominante concorda con il bounce
- **#12 FFT Regime**: regime CYCLE come gate opzionale (full_confl)
- LONG = bounce da supporto AND slope>0 AND [regime=CYCLE]

## Best Full Confluence (≥100 trade OOS)
- TF=M5  fp=5  tol=0.5  lb=30
- N=64  delta=0.05  min_p=10
- RR=2.0  Session=all
- Train PF=0.9082 | OOS PF=0.9425
- OOS DD=93.40%  OOS Trades=4201
- PF Gain=+0.096  DD Gain=+6.600

## Top 15 Full Confl

| # | TF | fp | tol | lb | N | δ | Sess | RR | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | all | 2.0 | 0.908 | 0.943 | 93.4 | 4201 | +0.096 |
| 2 | M5 | 5 | 0.5 | 30 | 64 | 0.03 | all | 2.0 | 0.888 | 0.942 | 94.7 | 4455 | +0.096 |
| 3 | M5 | 5 | 0.3 | 30 | 64 | 0.05 | london | 3.0 | 1.200 | 0.938 | 93.1 | 2344 | +0.046 |
| 4 | M5 | 5 | 0.5 | 30 | 64 | 0.03 | london | 3.0 | 1.044 | 0.937 | 99.0 | 4153 | +0.035 |
| 5 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | london | 3.0 | 1.056 | 0.936 | 98.8 | 3962 | +0.034 |
| 6 | M5 | 5 | 0.5 | 70 | 64 | 0.03 | london | 2.0 | 1.020 | 0.936 | 90.0 | 2900 | +0.058 |
| 7 | M5 | 5 | 0.3 | 30 | 64 | 0.03 | london | 3.0 | 1.198 | 0.935 | 94.4 | 2466 | +0.043 |
| 8 | M5 | 5 | 0.3 | 30 | 64 | 0.05 | all | 2.0 | 0.900 | 0.935 | 85.1 | 2513 | +0.088 |
| 9 | M5 | 5 | 0.3 | 30 | 64 | 0.03 | all | 2.0 | 0.887 | 0.931 | 85.6 | 2651 | +0.085 |
| 10 | M5 | 5 | 1.0 | 30 | 128 | 0.05 | newyork | 3.0 | 0.996 | 0.931 | 93.9 | 3039 | +0.051 |
| 11 | M5 | 5 | 0.5 | 70 | 64 | 0.05 | london | 2.0 | 1.018 | 0.930 | 88.7 | 2747 | +0.052 |
| 12 | M5 | 5 | 0.5 | 30 | 64 | 0.03 | london | 3.0 | 0.996 | 0.929 | 89.6 | 1698 | +0.027 |
| 13 | M5 | 5 | 1.0 | 30 | 128 | 0.05 | london | 3.0 | 0.854 | 0.929 | 94.3 | 3318 | +0.012 |
| 14 | M5 | 5 | 0.3 | 70 | 128 | 0.05 | london | 3.0 | 1.005 | 0.926 | 97.7 | 4724 | +0.025 |
| 15 | M5 | 5 | 1.0 | 30 | 128 | 0.03 | london | 3.0 | 0.962 | 0.924 | 99.9 | 8886 | +0.007 |
