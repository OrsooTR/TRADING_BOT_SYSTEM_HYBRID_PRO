# FFT Clock Trigger HFT Filter (#14) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-07-07 18:23:53 UTC  |  Combos: 208
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=128 ratio>0.08 pers>0.50 P=10
- Session=london | OOS PF=0.906
- PF Gain=+0.007 | OOS DD=97.0% | Trades=4448

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 128 | 0.08 | 0.50 | 10 | london | 0.875 | 0.906 | 97.0 | +0.007 | 3.2% |
| 2 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 10 | asian | 0.824 | 0.799 | 99.5 | +0.007 | 10.5% |
| 3 | rsi | fft_cloc | 64 | 0.06 | 0.50 | 10 | asian | 0.812 | 0.799 | 99.6 | +0.007 | 7.9% |
| 4 | rsi | fft_cloc | 64 | 0.08 | 0.50 | 10 | asian | 0.812 | 0.799 | 99.6 | +0.007 | 7.9% |
| 5 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 10 | london | 0.882 | 0.905 | 97.0 | +0.006 | 3.7% |
| 6 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 10 | asian | 0.824 | 0.798 | 99.6 | +0.006 | 10.4% |
| 7 | rsi | fft_cloc | 64 | 0.10 | 0.50 | 10 | asian | 0.812 | 0.797 | 99.6 | +0.006 | 7.8% |
| 8 | derivative | fft_cloc | 128 | 0.08 | 0.30 | 20 | london | 0.951 | 0.921 | 100.0 | +0.005 | 3.9% |
| 9 | rsi | fft_cloc | 128 | 0.10 | 0.50 | 10 | london | 0.881 | 0.903 | 97.3 | +0.005 | 2.1% |
| 10 | derivative | time_clo | 0 | 0.00 | 0.00 | 0 | asian | 0.836 | 0.815 | 100.0 | +0.004 | 8.3% |
