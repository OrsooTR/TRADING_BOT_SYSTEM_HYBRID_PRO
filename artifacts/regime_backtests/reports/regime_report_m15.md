# FFT Spectral Regime Classifier (#12) — M15

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
- RSI in noise | N=128 delta=0.08
- Session=london | OOS PF=1.224
- OOS DD=20.1%  | PF Gain vs baseline=0.176

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | rsi | noise | 128 | 0.08 | london | 1.046 | 1.224 | 20.1 | +0.176 |
| 2 | rsi | noise | 128 | 0.08 | london | 1.046 | 1.224 | 20.1 | +0.176 |
| 3 | rsi | noise | 128 | 0.03 | london | 1.153 | 1.177 | 24.2 | +0.129 |
| 4 | rsi | noise | 128 | 0.03 | london | 1.153 | 1.177 | 24.2 | +0.129 |
| 5 | rsi | noise | 128 | 0.05 | london | 0.923 | 1.155 | 22.0 | +0.107 |
| 6 | rsi | noise | 128 | 0.05 | london | 0.923 | 1.155 | 22.0 | +0.107 |
| 7 | derivative | cycle | 64 | 0.03 | asian | 0.975 | 1.065 | 66.7 | +0.027 |
| 8 | derivative | cycle | 64 | 0.03 | asian | 0.963 | 1.058 | 67.0 | +0.020 |
| 9 | derivative | cycle | 128 | 0.03 | asian | 0.941 | 1.040 | 80.4 | +0.000 |
| 10 | derivative | cycle | 128 | 0.05 | asian | 0.924 | 1.038 | 76.2 | -0.002 |
