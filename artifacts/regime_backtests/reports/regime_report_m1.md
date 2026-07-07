# FFT Spectral Regime Classifier (#12) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-05-11 07:45:38 UTC  |  Combos: 96
- Train: 2020  |  OOS: 2021-2025

## Logica
- FFT su log-return con Hann window
- Regime CYCLE: mid_ratio > hf_ratio + delta
- Regime NOISE: hf_ratio > mid_ratio + delta
- Regime TREND: spectral_slope < slope_thresh
- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE

## Best setup filtrato
- RSI in noise | N=64 delta=0.03
- Session=newyork | OOS PF=1.144
- OOS DD=53.7%  | PF Gain vs baseline=0.015

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | noise | 64 | 0.03 | newyork | 1.125 | 1.144 | 53.7 | +0.015 |
| 2 | rsi | noise | 64 | 0.03 | newyork | 1.127 | 1.144 | 53.7 | +0.015 |
| 3 | rsi | noise | 64 | 0.05 | newyork | 1.125 | 1.137 | 56.2 | +0.008 |
| 4 | rsi | noise | 64 | 0.05 | newyork | 1.128 | 1.137 | 56.2 | +0.008 |
| 5 | rsi | noise | 64 | 0.05 | asian | 1.036 | 1.131 | 56.5 | +0.047 |
| 6 | rsi | noise | 64 | 0.05 | asian | 1.036 | 1.130 | 56.5 | +0.047 |
| 7 | rsi | noise | 64 | 0.03 | asian | 1.075 | 1.126 | 60.0 | +0.042 |
| 8 | rsi | noise | 64 | 0.03 | asian | 1.075 | 1.125 | 60.0 | +0.042 |
| 9 | rsi | noise | 64 | 0.08 | newyork | 1.107 | 1.119 | 53.5 | -0.010 |
| 10 | rsi | noise | 64 | 0.08 | newyork | 1.110 | 1.119 | 53.5 | -0.010 |
