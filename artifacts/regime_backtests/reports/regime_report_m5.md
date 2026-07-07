# FFT Spectral Regime Classifier (#12) — M5

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-05-11 07:45:38 UTC  |  Combos: 192
- Train: 2020  |  OOS: 2021-2025

## Logica
- FFT su log-return con Hann window
- Regime CYCLE: mid_ratio > hf_ratio + delta
- Regime NOISE: hf_ratio > mid_ratio + delta
- Regime TREND: spectral_slope < slope_thresh
- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE

## Best setup filtrato
- RSI in noise | N=128 delta=0.03
- Session=london | OOS PF=1.199
- OOS DD=24.6%  | PF Gain vs baseline=0.189

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | noise | 128 | 0.03 | london | 0.818 | 1.199 | 24.6 | +0.189 |
| 2 | rsi | noise | 128 | 0.03 | london | 0.818 | 1.199 | 24.6 | +0.189 |
| 3 | rsi | noise | 128 | 0.05 | london | 0.851 | 1.186 | 23.0 | +0.176 |
| 4 | rsi | noise | 128 | 0.05 | london | 0.851 | 1.186 | 23.0 | +0.176 |
| 5 | rsi | noise | 128 | 0.08 | london | 0.938 | 1.177 | 15.9 | +0.167 |
| 6 | rsi | noise | 128 | 0.08 | london | 0.938 | 1.177 | 15.9 | +0.167 |
| 7 | rsi | noise | 64 | 0.03 | asian | 0.960 | 1.059 | 38.2 | +0.046 |
| 8 | rsi | noise | 64 | 0.03 | asian | 0.960 | 1.059 | 38.2 | +0.046 |
| 9 | rsi | noise | 64 | 0.05 | asian | 0.971 | 1.057 | 39.2 | +0.044 |
| 10 | rsi | noise | 64 | 0.05 | asian | 0.971 | 1.057 | 39.2 | +0.044 |
