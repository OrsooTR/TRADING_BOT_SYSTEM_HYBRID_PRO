# FFT Dominant Cycle (#11) — EURUSD ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-07-07 18:22:50 UTC  |  Combinations: 1152
- Train: 2020  |  OOS: 2021-2025

## Logic
- Rolling FFT on log-returns with Hann window (size N)
- Mid-band mask: exclude low_pct (trend) and high_pct (noise) bins
- Dominant bin = max energy in mid-band
- Quality filter: SNR > 1.5 AND dominant period > min_period bars
- Long:  cycle slope JUST turned positive (zero-crossing up)
- Short: cycle slope JUST turned negative (zero-crossing down)
- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr

## Best Setup
- TF=M15  N=256  low_pct=0.10  high_pct=0.20
- min_period=10b  SL_mult=1.5  RR=2.0  Session=newyork
- Train PF=0.9794  |  OOS PF=1.0990
- OOS DD=25.10%  |  OOS P&L=60.33%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 256 | 0.10 | 0.20 | 10 | 1.5 | 2.0 | newyork | 0.979 | 1.099 | 25.10 | 60.33 |
| 2 | M15 | 256 | 0.10 | 0.20 | 10 | 1.0 | 3.0 | newyork | 0.795 | 1.092 | 32.15 | 59.92 |
| 3 | M15 | 256 | 0.10 | 0.20 | 10 | 1.0 | 2.0 | newyork | 0.748 | 1.087 | 21.24 | 50.34 |
| 4 | M15 | 256 | 0.05 | 0.20 | 10 | 1.5 | 2.0 | newyork | 0.949 | 1.059 | 30.50 | 33.06 |
| 5 | M15 | 256 | 0.10 | 0.30 | 10 | 1.0 | 2.0 | newyork | 0.898 | 1.051 | 25.07 | 28.04 |
| 6 | M15 | 256 | 0.10 | 0.20 | 10 | 1.0 | 4.0 | newyork | 0.739 | 1.036 | 50.49 | 8.03 |
| 7 | M15 | 256 | 0.10 | 0.30 | 10 | 1.5 | 2.0 | newyork | 1.023 | 1.022 | 38.77 | 4.88 |
| 8 | M15 | 256 | 0.10 | 0.30 | 10 | 1.0 | 3.0 | newyork | 0.909 | 1.020 | 43.93 | 0.39 |
| 9 | M15 | 128 | 0.05 | 0.20 | 10 | 1.5 | 2.0 | london | 0.955 | 1.018 | 37.60 | 2.11 |
| 10 | M15 | 256 | 0.05 | 0.20 | 10 | 1.0 | 2.0 | newyork | 0.711 | 1.014 | 28.12 | -0.70 |
