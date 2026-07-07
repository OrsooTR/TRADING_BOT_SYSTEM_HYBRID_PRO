# FFT Dominant Cycle (#11) — EURUSD ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-05-08 07:47:37 UTC  |  Combinations: 1152
- Train: 2020-2023  |  OOS: 2024-2025

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
- min_period=10b  SL_mult=1.0  RR=2.0  Session=london
- Train PF=0.8933  |  OOS PF=1.1732
- OOS DD=16.13%  |  OOS P&L=160.74%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M15 | 256 | 0.10 | 0.20 | 10 | 1.0 | 2.0 | london | 0.893 | 1.173 | 16.13 | 160.74 |
| 2 | M15 | 256 | 0.10 | 0.20 | 10 | 1.0 | 3.0 | london | 0.970 | 1.161 | 33.42 | 165.17 |
| 3 | M15 | 256 | 0.10 | 0.30 | 10 | 1.0 | 2.0 | london | 0.994 | 1.137 | 19.63 | 145.80 |
| 4 | M15 | 128 | 0.05 | 0.20 | 10 | 1.5 | 2.0 | asian | 1.029 | 1.128 | 23.77 | 104.67 |
| 5 | M15 | 128 | 0.05 | 0.20 | 10 | 1.0 | 3.0 | asian | 0.975 | 1.126 | 25.68 | 114.33 |
| 6 | M15 | 256 | 0.10 | 0.20 | 10 | 1.5 | 2.0 | london | 1.078 | 1.122 | 22.69 | 93.44 |
| 7 | M15 | 128 | 0.10 | 0.30 | 10 | 1.0 | 4.0 | asian | 0.837 | 1.120 | 41.33 | 124.32 |
| 8 | M15 | 128 | 0.05 | 0.30 | 10 | 1.0 | 3.0 | asian | 0.995 | 1.119 | 30.03 | 140.22 |
| 9 | M15 | 128 | 0.05 | 0.20 | 10 | 1.0 | 4.0 | asian | 1.048 | 1.116 | 29.47 | 101.34 |
| 10 | M15 | 256 | 0.05 | 0.20 | 10 | 1.0 | 2.0 | london | 0.877 | 1.114 | 21.20 | 100.64 |
