# FFT Clock Trigger HFT Filter (#14) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-07-07 18:23:53 UTC  |  Combos: 112
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=64 ratio>0.08 pers>0.50 P=10
- Session=london | OOS PF=0.825
- PF Gain=+0.006 | OOS DD=100.0% | Trades=18247

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 64 | 0.08 | 0.50 | 10 | london | 0.830 | 0.825 | 100.0 | +0.006 | 4.1% |
| 2 | rsi | fft_cloc | 64 | 0.06 | 0.50 | 10 | london | 0.830 | 0.825 | 100.0 | +0.006 | 4.1% |
| 3 | rsi | fft_cloc | 64 | 0.10 | 0.50 | 10 | london | 0.829 | 0.825 | 100.0 | +0.006 | 3.9% |
| 4 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 10 | newyork | 0.874 | 0.780 | 100.0 | +0.006 | 5.4% |
| 5 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 20 | london | 0.826 | 0.824 | 100.0 | +0.005 | 5.5% |
| 6 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 10 | newyork | 0.874 | 0.780 | 100.0 | +0.005 | 5.2% |
| 7 | rsi | fft_cloc | 64 | 0.10 | 0.30 | 10 | newyork | 0.874 | 0.780 | 100.0 | +0.005 | 4.9% |
| 8 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 10 | london | 0.831 | 0.824 | 100.0 | +0.005 | 5.2% |
| 9 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 10 | london | 0.830 | 0.824 | 100.0 | +0.005 | 5.4% |
| 10 | rsi | fft_cloc | 64 | 0.10 | 0.30 | 10 | london | 0.830 | 0.823 | 100.0 | +0.005 | 4.9% |
