# FFT Clock Trigger HFT Filter (#14) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-05-11 08:20:20 UTC  |  Combos: 528
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=128 ratio>0.06 pers>0.30 P=10
- Session=newyork | OOS PF=1.022
- PF Gain=+0.065 | OOS DD=32.6% | Trades=541

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 10 | newyork | 1.128 | 1.022 | 32.6 | +0.065 | 10.0% |
| 2 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 20 | newyork | 1.184 | 1.019 | 29.2 | +0.062 | 18.7% |
| 3 | rsi | fft_cloc | 64 | 0.10 | 0.30 | 20 | newyork | 1.169 | 1.018 | 29.9 | +0.061 | 17.4% |
| 4 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 20 | newyork | 1.103 | 1.017 | 33.3 | +0.059 | 10.8% |
| 5 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 10 | newyork | 1.086 | 1.016 | 32.7 | +0.059 | 8.9% |
| 6 | rsi | fft_cloc | 128 | 0.06 | 0.50 | 10 | newyork | 1.139 | 1.014 | 32.0 | +0.057 | 8.7% |
| 7 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 20 | newyork | 1.184 | 1.012 | 29.9 | +0.055 | 18.3% |
| 8 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 20 | newyork | 1.086 | 1.008 | 34.0 | +0.051 | 9.1% |
| 9 | rsi | fft_cloc | 128 | 0.08 | 0.50 | 10 | newyork | 1.098 | 1.008 | 32.1 | +0.051 | 7.8% |
| 10 | rsi | fft_cloc | 128 | 0.06 | 0.50 | 20 | newyork | 1.060 | 1.005 | 36.6 | +0.048 | 8.3% |
