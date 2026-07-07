# Fractal + FFT Confluence (#18) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

- Generated: 2026-05-11 08:59:08 UTC  |  Combos totali: 432
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#05 Fractal S/R**: pivot Williams → livelli attivi nella finestra lookback
- **#11 FFT Cycle**: slope del ciclo dominante concorda con il bounce
- **#12 FFT Regime**: regime CYCLE come gate opzionale (full_confl)
- LONG = bounce da supporto AND slope>0 AND [regime=CYCLE]

## Best Full Confluence (≥100 trade OOS)
- TF=M1  fp=5  tol=0.3  lb=30
- N=64  delta=0.05  min_p=5
- RR=2.0  Session=newyork
- Train PF=0.8481 | OOS PF=1.0198
- OOS DD=78.37%  OOS Trades=9865
- PF Gain=-0.010  DD Gain=+20.160

## Top 15 Full Confl

| # | TF | fp | tol | lb | N | δ | Sess | RR | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 5 | 0.3 | 30 | 64 | 0.05 | newyork | 2.0 | 0.848 | 1.020 | 78.4 | 9865 | -0.010 |
| 2 | M1 | 5 | 0.3 | 30 | 64 | 0.03 | newyork | 2.0 | 0.844 | 1.015 | 81.6 | 10426 | -0.015 |
| 3 | M1 | 5 | 1.0 | 30 | 64 | 0.05 | newyork | 2.0 | 0.963 | 1.008 | 99.6 | 29700 | +0.000 |
| 4 | M1 | 5 | 1.0 | 30 | 64 | 0.03 | newyork | 2.0 | 0.965 | 1.007 | 99.7 | 31296 | -0.001 |
| 5 | M1 | 5 | 0.5 | 30 | 64 | 0.05 | newyork | 2.0 | 0.916 | 1.001 | 94.3 | 15452 | -0.017 |
| 6 | M1 | 5 | 0.5 | 30 | 64 | 0.03 | newyork | 2.0 | 0.912 | 0.999 | 95.2 | 16307 | -0.020 |
| 7 | M1 | 5 | 0.3 | 70 | 64 | 0.05 | newyork | 2.0 | 0.870 | 0.993 | 96.6 | 17304 | +0.005 |
| 8 | M1 | 5 | 0.3 | 30 | 64 | 0.03 | asian | 2.0 | 1.005 | 0.993 | 93.4 | 11101 | +0.013 |
| 9 | M1 | 5 | 0.3 | 30 | 64 | 0.05 | newyork | 2.0 | 0.811 | 0.993 | 67.9 | 4187 | -0.037 |
| 10 | M1 | 5 | 0.3 | 30 | 64 | 0.05 | asian | 2.0 | 0.998 | 0.992 | 92.0 | 10562 | +0.013 |
| 11 | M1 | 5 | 1.0 | 70 | 64 | 0.05 | newyork | 2.0 | 0.954 | 0.991 | 100.0 | 46060 | +0.012 |
| 12 | M1 | 5 | 0.3 | 70 | 64 | 0.03 | asian | 2.0 | 0.972 | 0.991 | 98.8 | 19899 | +0.011 |
| 13 | M1 | 5 | 1.0 | 70 | 64 | 0.03 | newyork | 2.0 | 0.960 | 0.990 | 100.0 | 48481 | +0.010 |
| 14 | M1 | 5 | 0.3 | 70 | 64 | 0.03 | newyork | 2.0 | 0.879 | 0.989 | 97.6 | 18253 | +0.001 |
| 15 | M1 | 5 | 0.3 | 70 | 64 | 0.05 | asian | 2.0 | 0.973 | 0.988 | 98.8 | 18929 | +0.008 |
