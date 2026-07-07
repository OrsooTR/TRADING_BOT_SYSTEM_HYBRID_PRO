# FFT Spectral Regime Classifier (#12) — ALL_TFS

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-05-11 07:45:38 UTC  |  Combos: 480
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
| 3 | rsi | noise | 128 | 0.03 | london | 0.818 | 1.199 | 24.6 | +0.189 |
| 4 | rsi | noise | 128 | 0.03 | london | 0.818 | 1.199 | 24.6 | +0.189 |
| 5 | rsi | noise | 128 | 0.05 | london | 0.851 | 1.186 | 23.0 | +0.176 |
| 6 | rsi | noise | 128 | 0.05 | london | 0.851 | 1.186 | 23.0 | +0.176 |
| 7 | rsi | noise | 128 | 0.08 | london | 0.938 | 1.177 | 15.9 | +0.167 |
| 8 | rsi | noise | 128 | 0.08 | london | 0.938 | 1.177 | 15.9 | +0.167 |
| 9 | rsi | noise | 128 | 0.03 | london | 1.153 | 1.177 | 24.2 | +0.129 |
| 10 | rsi | noise | 128 | 0.03 | london | 1.153 | 1.177 | 24.2 | +0.129 |
