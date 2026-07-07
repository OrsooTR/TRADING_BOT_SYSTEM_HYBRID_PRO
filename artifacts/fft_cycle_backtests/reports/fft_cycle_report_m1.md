# FFT Dominant Cycle (#11) — EURUSD M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-05-08 07:47:37 UTC  |  Combinations: 192
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
- TF=M1  N=64  low_pct=0.10  high_pct=0.30
- min_period=10b  SL_mult=1.0  RR=3.0  Session=newyork
- Train PF=1.0814  |  OOS PF=1.1105
- OOS DD=63.88%  |  OOS P&L=163839355.13%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 64 | 0.10 | 0.30 | 10 | 1.0 | 3.0 | newyork | 1.081 | 1.111 | 63.88 | 163839355.13 |
| 2 | M1 | 64 | 0.10 | 0.20 | 5 | 1.0 | 3.0 | newyork | 1.095 | 1.109 | 65.98 | 1993501743592413593600.00 |
| 3 | M1 | 64 | 0.10 | 0.20 | 10 | 1.0 | 3.0 | newyork | 1.094 | 1.108 | 57.97 | 18529055.26 |
| 4 | M1 | 64 | 0.10 | 0.30 | 5 | 1.0 | 3.0 | newyork | 1.092 | 1.107 | 71.76 | 495638457048858525433856.00 |
| 5 | M1 | 64 | 0.10 | 0.30 | 10 | 1.0 | 2.0 | newyork | 1.121 | 1.104 | 54.18 | 28712655.70 |
| 6 | M1 | 64 | 0.10 | 0.20 | 10 | 1.0 | 2.0 | newyork | 1.143 | 1.104 | 46.75 | 5325750.68 |
| 7 | M1 | 64 | 0.05 | 0.20 | 5 | 1.0 | 3.0 | newyork | 1.101 | 1.103 | 67.28 | 132089841733616959488.00 |
| 8 | M1 | 64 | 0.05 | 0.30 | 5 | 1.0 | 3.0 | newyork | 1.097 | 1.101 | 69.25 | 15375336134706930384896.00 |
| 9 | M1 | 64 | 0.10 | 0.20 | 5 | 1.0 | 4.0 | newyork | 1.084 | 1.097 | 79.77 | 5030252898111259648.00 |
| 10 | M1 | 64 | 0.10 | 0.30 | 5 | 1.0 | 4.0 | newyork | 1.089 | 1.097 | 77.65 | 1482165064829989289984.00 |
