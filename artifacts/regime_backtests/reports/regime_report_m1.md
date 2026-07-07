# FFT Spectral Regime Classifier (#12) — M1

- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

- Generated: 2026-07-07 18:22:52 UTC  |  Combos: 96
- Train: 2020  |  OOS: 2021-2025

## Logica
- FFT su log-return con Hann window
- Regime CYCLE: mid_ratio > hf_ratio + delta
- Regime NOISE: hf_ratio > mid_ratio + delta
- Regime TREND: spectral_slope < slope_thresh
- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE

## Best setup filtrato
- DERIVATIVE in cycle | N=64 delta=0.05
- Session=london | OOS PF=0.830
- OOS DD=100.0%  | PF Gain vs baseline=0.008

## Top 10 filtrati

| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|---|---|---|---|---|---|---|---|---|
| 1 | derivative | cycle | 64 | 0.05 | london | 0.870 | 0.830 | 100.0 | +0.008 |
| 2 | derivative | cycle | 64 | 0.08 | london | 0.861 | 0.830 | 100.0 | +0.008 |
| 3 | derivative | cycle | 64 | 0.03 | london | 0.869 | 0.830 | 100.0 | +0.007 |
| 4 | derivative | cycle | 64 | 0.05 | london | 0.874 | 0.829 | 100.0 | +0.006 |
| 5 | derivative | cycle | 64 | 0.03 | london | 0.873 | 0.828 | 100.0 | +0.006 |
| 6 | derivative | cycle | 64 | 0.08 | london | 0.866 | 0.828 | 100.0 | +0.006 |
| 7 | rsi | noise | 64 | 0.03 | london | 0.879 | 0.825 | 100.0 | +0.006 |
| 8 | rsi | noise | 64 | 0.03 | london | 0.878 | 0.825 | 100.0 | +0.006 |
| 9 | rsi | noise | 64 | 0.05 | london | 0.863 | 0.824 | 100.0 | +0.005 |
| 10 | rsi | noise | 64 | 0.05 | london | 0.863 | 0.824 | 100.0 | +0.005 |
