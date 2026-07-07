# FFT Clock Trigger HFT Filter (#14) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-05-11 08:20:20 UTC  |  Combos: 208
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=128 ratio>0.08 pers>0.30 P=10
- Session=asian | OOS PF=1.019
- PF Gain=+0.006 | OOS DD=55.5% | Trades=3644

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 10 | asian | 1.066 | 1.019 | 55.5 | +0.006 | 3.7% |
| 2 | rsi | time_clo | 0 | 0.00 | 0.00 | 0 | newyork | 1.058 | 0.992 | 65.7 | +0.006 | 8.3% |
| 3 | derivative | time_clo | 0 | 0.00 | 0.00 | 0 | newyork | 0.858 | 0.912 | 100.0 | +0.006 | 8.3% |
| 4 | rsi | fft_cloc | 128 | 0.08 | 0.50 | 10 | asian | 1.057 | 1.018 | 57.7 | +0.006 | 3.2% |
| 5 | rsi | fft_cloc | 128 | 0.10 | 0.50 | 10 | asian | 1.059 | 1.018 | 56.1 | +0.005 | 2.1% |
| 6 | derivative | time_clo | 0 | 0.00 | 0.00 | 0 | all | 0.956 | 0.973 | 100.0 | +0.004 | 8.3% |
| 7 | derivative | fft_cloc | 128 | 0.06 | 0.30 | 20 | newyork | 0.861 | 0.910 | 100.0 | +0.004 | 4.7% |
| 8 | rsi | fft_cloc | 128 | 0.10 | 0.30 | 10 | asian | 1.063 | 1.017 | 54.7 | +0.004 | 2.4% |
| 9 | derivative | fft_cloc | 128 | 0.08 | 0.50 | 10 | london | 0.917 | 0.991 | 99.8 | +0.004 | 3.2% |
| 10 | derivative | fft_cloc | 128 | 0.08 | 0.30 | 10 | london | 0.916 | 0.991 | 99.8 | +0.004 | 3.7% |
