# FFT Dominant Cycle (#11) — EURUSD M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]

- Generated: 2026-07-07 18:22:50 UTC  |  Combinations: 192
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
- TF=M1  N=64  low_pct=0.05  high_pct=0.30
- min_period=5b  SL_mult=1.5  RR=4.0  Session=london
- Train PF=0.8671  |  OOS PF=0.8379
- OOS DD=100.00%  |  OOS P&L=-100.00%

## Top 10

| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | 64 | 0.05 | 0.30 | 5 | 1.5 | 4.0 | london | 0.867 | 0.838 | 100.00 | -100.00 |
| 2 | M1 | 64 | 0.10 | 0.30 | 5 | 1.5 | 4.0 | london | 0.869 | 0.836 | 100.00 | -100.00 |
| 3 | M1 | 64 | 0.05 | 0.20 | 5 | 1.5 | 4.0 | london | 0.871 | 0.835 | 100.00 | -100.00 |
| 4 | M1 | 64 | 0.10 | 0.20 | 5 | 1.5 | 4.0 | london | 0.875 | 0.834 | 100.00 | -100.00 |
| 5 | M1 | 64 | 0.10 | 0.20 | 10 | 1.5 | 4.0 | london | 0.910 | 0.830 | 100.00 | -100.00 |
| 6 | M1 | 64 | 0.05 | 0.20 | 10 | 1.5 | 4.0 | london | 0.877 | 0.828 | 100.00 | -100.00 |
| 7 | M1 | 64 | 0.05 | 0.30 | 10 | 1.5 | 4.0 | london | 0.875 | 0.826 | 100.00 | -100.00 |
| 8 | M1 | 64 | 0.10 | 0.30 | 10 | 1.5 | 4.0 | london | 0.908 | 0.824 | 100.00 | -100.00 |
| 9 | M1 | 64 | 0.05 | 0.30 | 5 | 1.5 | 3.0 | london | 0.851 | 0.822 | 100.00 | -100.00 |
| 10 | M1 | 64 | 0.05 | 0.20 | 5 | 1.5 | 3.0 | london | 0.852 | 0.821 | 100.00 | -100.00 |
