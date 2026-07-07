# FFT Clock Trigger HFT Filter (#14) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-05-11 08:20:20 UTC  |  Combos: 112
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=64 ratio>0.06 pers>0.30 P=20
- Session=asian | OOS PF=1.094
- PF Gain=+0.011 | OOS DD=69.8% | Trades=16221

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 20 | asian | 1.079 | 1.094 | 69.8 | +0.011 | 5.5% |
| 2 | rsi | fft_cloc | 64 | 0.08 | 0.50 | 10 | asian | 1.086 | 1.093 | 68.3 | +0.010 | 4.1% |
| 3 | rsi | fft_cloc | 64 | 0.06 | 0.50 | 10 | asian | 1.086 | 1.093 | 68.3 | +0.010 | 4.1% |
| 4 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 10 | asian | 1.083 | 1.092 | 67.9 | +0.009 | 5.2% |
| 5 | rsi | fft_cloc | 64 | 0.10 | 0.50 | 10 | asian | 1.085 | 1.092 | 69.2 | +0.009 | 3.9% |
| 6 | rsi | fft_cloc | 64 | 0.08 | 0.30 | 20 | asian | 1.081 | 1.092 | 70.1 | +0.009 | 5.0% |
| 7 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 10 | asian | 1.081 | 1.092 | 67.9 | +0.009 | 5.4% |
| 8 | rsi | fft_cloc | 64 | 0.10 | 0.30 | 10 | asian | 1.082 | 1.092 | 68.9 | +0.008 | 4.9% |
| 9 | rsi | fft_cloc | 64 | 0.10 | 0.30 | 20 | asian | 1.081 | 1.092 | 71.3 | +0.008 | 4.4% |
| 10 | rsi | fft_cloc | 64 | 0.06 | 0.30 | 10 | london | 1.133 | 1.081 | 69.2 | +0.007 | 5.4% |
