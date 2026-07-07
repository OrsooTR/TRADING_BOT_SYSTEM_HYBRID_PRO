# FFT Clock Trigger HFT Filter (#14) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

- Generated: 2026-07-07 18:23:53 UTC  |  Combos: 528
- Train: 2020  |  OOS: 2021-2025

## Logica
- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario
- Persistence = frac finestre dove bin clock è dominante
- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry
- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)

## Best setup
- RSI | filter=fft_clock
- N=128 ratio>0.06 pers>0.30 P=20
- Session=london | OOS PF=0.937
- PF Gain=+0.041 | OOS DD=70.3% | Trades=1612

## Top 10

| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 20 | london | 0.824 | 0.937 | 70.3 | +0.041 | 10.8% |
| 2 | rsi | fft_cloc | 128 | 0.06 | 0.50 | 20 | london | 0.830 | 0.937 | 71.5 | +0.041 | 8.3% |
| 3 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 20 | all | 0.907 | 0.943 | 82.2 | +0.031 | 10.8% |
| 4 | rsi | fft_cloc | 128 | 0.06 | 0.50 | 10 | london | 0.831 | 0.925 | 73.2 | +0.029 | 8.7% |
| 5 | rsi | fft_cloc | 128 | 0.08 | 0.50 | 20 | london | 0.858 | 0.925 | 74.4 | +0.029 | 7.4% |
| 6 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 10 | london | 0.837 | 0.925 | 73.3 | +0.029 | 10.0% |
| 7 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 20 | london | 0.860 | 0.925 | 74.0 | +0.029 | 9.1% |
| 8 | rsi | fft_cloc | 128 | 0.08 | 0.30 | 10 | london | 0.858 | 0.924 | 73.8 | +0.029 | 8.9% |
| 9 | rsi | fft_cloc | 128 | 0.06 | 0.30 | 20 | newyork | 0.890 | 1.043 | 45.1 | +0.028 | 10.8% |
| 10 | rsi | fft_cloc | 128 | 0.06 | 0.50 | 20 | all | 0.899 | 0.939 | 85.0 | +0.028 | 8.3% |
