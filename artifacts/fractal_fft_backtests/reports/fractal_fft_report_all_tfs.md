# Fractal + FFT Confluence (#18) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

- Generated: 2026-05-11 08:59:08 UTC  |  Combos totali: 1248
- Train: 2020  |  OOS: 2021-2025

## Logica
- **#05 Fractal S/R**: pivot Williams → livelli attivi nella finestra lookback
- **#11 FFT Cycle**: slope del ciclo dominante concorda con il bounce
- **#12 FFT Regime**: regime CYCLE come gate opzionale (full_confl)
- LONG = bounce da supporto AND slope>0 AND [regime=CYCLE]

## Best Full Confluence (≥100 trade OOS)
- TF=M5  fp=5  tol=0.5  lb=30
- N=64  delta=0.05  min_p=10
- RR=2.0  Session=newyork
- Train PF=0.8659 | OOS PF=1.2679
- OOS DD=37.06%  OOS Trades=1372
- PF Gain=+0.238  DD Gain=+62.660

## Top 15 Full Confl

| # | TF | fp | tol | lb | N | δ | Sess | RR | Train PF | OOS PF | OOS DD% | Trades | PF Gain |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | newyork | 2.0 | 0.866 | 1.268 | 37.1 | 1372 | +0.238 |
| 2 | M5 | 5 | 0.5 | 30 | 64 | 0.03 | newyork | 2.0 | 0.893 | 1.248 | 40.1 | 1448 | +0.218 |
| 3 | M5 | 5 | 0.3 | 30 | 64 | 0.05 | asian | 2.0 | 0.874 | 1.232 | 26.0 | 842 | +0.238 |
| 4 | M5 | 5 | 0.3 | 30 | 64 | 0.03 | asian | 2.0 | 0.860 | 1.225 | 23.0 | 890 | +0.230 |
| 5 | M5 | 5 | 0.3 | 30 | 64 | 0.05 | newyork | 2.0 | 0.816 | 1.205 | 34.8 | 858 | +0.145 |
| 6 | M5 | 5 | 0.3 | 30 | 64 | 0.03 | newyork | 2.0 | 0.863 | 1.183 | 38.0 | 897 | +0.122 |
| 7 | M5 | 5 | 0.5 | 30 | 64 | 0.03 | asian | 2.0 | 0.922 | 1.164 | 41.2 | 1545 | +0.161 |
| 8 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | asian | 2.0 | 0.965 | 1.164 | 38.0 | 1450 | +0.161 |
| 9 | M5 | 5 | 0.3 | 30 | 64 | 0.03 | asian | 3.0 | 0.808 | 1.150 | 37.9 | 890 | +0.138 |
| 10 | M5 | 5 | 0.3 | 30 | 64 | 0.05 | asian | 3.0 | 0.835 | 1.145 | 37.8 | 842 | +0.133 |
| 11 | M5 | 5 | 0.3 | 70 | 64 | 0.03 | asian | 2.0 | 1.081 | 1.145 | 36.0 | 1571 | +0.141 |
| 12 | M5 | 5 | 0.5 | 70 | 64 | 0.05 | newyork | 2.0 | 0.910 | 1.134 | 49.8 | 2064 | +0.136 |
| 13 | M5 | 5 | 0.3 | 70 | 64 | 0.05 | asian | 2.0 | 1.067 | 1.134 | 35.9 | 1484 | +0.130 |
| 14 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | newyork | 2.0 | 0.898 | 1.127 | 51.1 | 3511 | +0.097 |
| 15 | M5 | 5 | 0.5 | 30 | 64 | 0.05 | asian | 3.0 | 1.006 | 1.124 | 51.1 | 1450 | +0.118 |
