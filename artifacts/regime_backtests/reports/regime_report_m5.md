# FFT Spectral Regime Classifier (#12) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-07-07 18:22:52 UTC  |  Combos: 192
- Train: 2020  |  OOS: 2021-2025

## Logica
- FFT su log-return con Hann window
- Regime CYCLE: mid_ratio > hf_ratio + delta
- Regime NOISE: hf_ratio > mid_ratio + delta
- Regime TREND: spectral_slope < slope_thresh
- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE

## Best setup filtrato
- RSI in noise | N=128 delta=0.03
- Session=newyork | OOS PF=1.064
- OOS DD=23.4%  | PF Gain vs baseline=0.158

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | noise | 128 | 0.03 | newyork | 0.691 | 1.064 | 23.4 | +0.158 |
| 2 | rsi | noise | 128 | 0.03 | newyork | 0.691 | 1.064 | 23.4 | +0.158 |
| 3 | rsi | noise | 128 | 0.05 | newyork | 0.732 | 1.046 | 21.1 | +0.140 |
| 4 | rsi | noise | 128 | 0.05 | newyork | 0.732 | 1.046 | 21.1 | +0.140 |
| 5 | rsi | noise | 128 | 0.08 | newyork | 0.735 | 1.038 | 23.8 | +0.132 |
| 6 | rsi | noise | 128 | 0.08 | newyork | 0.735 | 1.038 | 23.8 | +0.132 |
| 7 | rsi | noise | 128 | 0.05 | london | 0.908 | 0.952 | 49.1 | +0.052 |
| 8 | rsi | noise | 128 | 0.05 | london | 0.908 | 0.952 | 49.1 | +0.052 |
| 9 | derivative | cycle | 128 | 0.08 | london | 0.942 | 0.941 | 100.0 | +0.026 |
| 10 | derivative | cycle | 128 | 0.08 | london | 0.937 | 0.940 | 100.0 | +0.024 |
