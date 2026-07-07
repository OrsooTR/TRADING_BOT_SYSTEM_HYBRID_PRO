# FFT Dominant Cycle (#11) — EURUSD M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-05-08 07:47:37 UTC  |  Combinations: 384
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
- TF=M5  N=64  low_pct=0.05  high_pct=0.30
- min_period=10b  SL_mult=1.0  RR=4.0  Session=london
- Train PF=0.8832  |  OOS PF=1.0636
- OOS DD=82.05%  |  OOS P&L=525.53%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M5 | 64 | 0.05 | 0.30 | 10 | 1.0 | 4.0 | london | 0.883 | 1.064 | 82.05 | 525.53 |
| 2 | M5 | 128 | 0.05 | 0.30 | 10 | 1.0 | 3.0 | london | 0.897 | 1.057 | 42.27 | 240.40 |
| 3 | M5 | 64 | 0.05 | 0.20 | 10 | 1.0 | 2.0 | london | 0.969 | 1.057 | 53.13 | 329.01 |
| 4 | M5 | 128 | 0.05 | 0.20 | 5 | 1.0 | 3.0 | asian | 1.036 | 1.056 | 74.23 | 3760.96 |
| 5 | M5 | 128 | 0.05 | 0.30 | 5 | 1.0 | 3.0 | asian | 1.046 | 1.055 | 63.73 | 6102.89 |
| 6 | M5 | 128 | 0.05 | 0.20 | 5 | 1.0 | 4.0 | asian | 1.052 | 1.055 | 88.96 | 2346.30 |
| 7 | M5 | 64 | 0.05 | 0.30 | 10 | 1.0 | 2.0 | london | 1.005 | 1.054 | 53.29 | 375.89 |
| 8 | M5 | 64 | 0.10 | 0.30 | 10 | 1.5 | 3.0 | london | 1.025 | 1.054 | 64.50 | 268.40 |
| 9 | M5 | 64 | 0.05 | 0.30 | 10 | 1.0 | 3.0 | london | 0.924 | 1.053 | 78.42 | 334.36 |
| 10 | M5 | 64 | 0.10 | 0.20 | 10 | 1.5 | 2.0 | london | 0.954 | 1.052 | 55.69 | 199.32 |
