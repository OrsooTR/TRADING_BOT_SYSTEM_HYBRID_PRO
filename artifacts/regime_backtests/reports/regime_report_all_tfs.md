# FFT Spectral Regime Classifier (#12) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-07-07 18:22:52 UTC  |  Combos: 480
- Train: 2020  |  OOS: 2021-2025

## Logica
- FFT su log-return con Hann window
- Regime CYCLE: mid_ratio > hf_ratio + delta
- Regime NOISE: hf_ratio > mid_ratio + delta
- Regime TREND: spectral_slope < slope_thresh
- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE

## Best setup filtrato
- RSI in noise | N=128 delta=0.08
- Session=newyork | OOS PF=1.220
- OOS DD=19.1%  | PF Gain vs baseline=0.204

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | noise | 128 | 0.08 | newyork | 1.137 | 1.220 | 19.1 | +0.204 |
| 2 | rsi | noise | 128 | 0.08 | newyork | 1.137 | 1.220 | 19.1 | +0.204 |
| 3 | rsi | noise | 128 | 0.03 | newyork | 1.145 | 1.185 | 23.0 | +0.171 |
| 4 | rsi | noise | 128 | 0.03 | newyork | 1.145 | 1.185 | 23.0 | +0.171 |
| 5 | rsi | noise | 128 | 0.05 | newyork | 0.969 | 1.164 | 21.1 | +0.149 |
| 6 | rsi | noise | 128 | 0.05 | newyork | 0.969 | 1.164 | 21.1 | +0.149 |
| 7 | rsi | noise | 128 | 0.03 | newyork | 0.691 | 1.064 | 23.4 | +0.158 |
| 8 | rsi | noise | 128 | 0.03 | newyork | 0.691 | 1.064 | 23.4 | +0.158 |
| 9 | rsi | noise | 128 | 0.05 | newyork | 0.732 | 1.046 | 21.1 | +0.140 |
| 10 | rsi | noise | 128 | 0.05 | newyork | 0.732 | 1.046 | 21.1 | +0.140 |
