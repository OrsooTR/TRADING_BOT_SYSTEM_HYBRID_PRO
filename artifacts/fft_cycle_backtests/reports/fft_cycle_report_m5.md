# FFT Dominant Cycle (#11) — EURUSD M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-07-07 18:22:50 UTC  |  Combinations: 384
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
- TF=M5  N=64  low_pct=0.10  high_pct=0.30
- min_period=10b  SL_mult=1.5  RR=3.0  Session=newyork
- Train PF=0.8694  |  OOS PF=0.9523
- OOS DD=95.41%  |  OOS P&L=-91.50%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 64 | 0.10 | 0.30 | 10 | 1.5 | 3.0 | newyork | 0.869 | 0.952 | 95.41 | -91.50 |
| 2 | M5 | 64 | 0.10 | 0.20 | 10 | 1.5 | 3.0 | newyork | 0.847 | 0.950 | 94.92 | -89.25 |
| 3 | M5 | 64 | 0.10 | 0.20 | 10 | 1.5 | 4.0 | newyork | 0.786 | 0.949 | 97.00 | -92.33 |
| 4 | M5 | 64 | 0.05 | 0.30 | 10 | 1.5 | 3.0 | newyork | 0.823 | 0.948 | 96.58 | -95.39 |
| 5 | M5 | 64 | 0.05 | 0.30 | 10 | 1.5 | 4.0 | newyork | 0.768 | 0.941 | 98.48 | -97.78 |
| 6 | M5 | 64 | 0.05 | 0.20 | 10 | 1.5 | 3.0 | newyork | 0.817 | 0.941 | 96.22 | -94.85 |
| 7 | M5 | 64 | 0.10 | 0.30 | 10 | 1.5 | 4.0 | newyork | 0.804 | 0.940 | 98.09 | -96.27 |
| 8 | M5 | 64 | 0.05 | 0.20 | 10 | 1.5 | 4.0 | newyork | 0.774 | 0.940 | 97.84 | -96.62 |
| 9 | M5 | 128 | 0.05 | 0.30 | 10 | 1.5 | 2.0 | london | 0.868 | 0.924 | 95.88 | -94.81 |
| 10 | M5 | 64 | 0.10 | 0.20 | 10 | 1.5 | 2.0 | newyork | 0.809 | 0.923 | 95.09 | -92.76 |
