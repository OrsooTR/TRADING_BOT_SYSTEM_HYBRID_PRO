# Strategie - INDEX

## Collegamenti

- [[../00_CORE/00_Regole_Progettazione]]
- [[../04_BACKTEST/INDEX]]
- [[../05_METRICS/INDEX]]
- [[../11_MEMORY/PROJECT_STATE]]
- [[../15_ARTIFACTS/INDEX]]

## Strategie testate

| # | Nome | Status | Best PF | TF | Note |
|---|------|--------|---------|----|------|
| 01 | [[TESTED/01_MA_Crossover]] | Completato | 1.13 | M1 | Regime filter, non entry |
| 02 | [[TESTED/02_Derivative_1st_2nd_Order]] | Completato | 2.70 | M5 | Forte segnale momentum |
| 03 | [[TESTED/03_RSI_MeanReversion]] | Completato | 1.59 | M1 | Robusto: 77% profittevoli |
| 04 | [[TESTED/04_BB_Squeeze]] | Completato | 1.22 | M15 | Edge debole, utile come filtro regime |
| 05 | [[TESTED/05_Fractal_SR_Bounce]] | Completato | 1.18 | M1 | 68% profittevoli, secondo dopo RSI |
| 06 | [[TESTED/06_VWAP_TrendTrading]] | Completato | 1.16 | M1 | Sessione LonNY, pure mode fedele paper |
| 07 | [[TESTED/07_ATR_Channel_Breakout]] | Completato | 1.20 | M15 | 10% profittevoli, debole — regime filter |
| 08 | [[TESTED/08_EMA_Ribbon_Direction]] | Completato | 1.20 | M15 | 30% profittevoli, filtro direzionale London |
| 11 | [[TESTED/11_FFT_Dominant_Cycle]] | Completato | 1.17 | M15 | 52% profittevoli, London N=256, prerequisito Layer FFT |
| 15 | [[TESTED/15_Volatility_Regime_Gate]] | Completato | 1.40 | M5 | Meta-filtro: forte su RSI low-vol, debole su Derivate high-vol |

## Strategie in backlog

| # | Nome | Status | Note |
|---|------|--------|------|
| 07 | [[IDEAS/atr_channel_breakout|ATR Channel Breakout]] | Da specificare | Breakout su canale ATR |
| 08 | VWAP Session Mean-Rev | Da specificare | Variante mean-reversion |
| 09 | FFT Cycle Prediction | Da specificare | Base del sistema finale |
| 10 | EMA Ribbon Direction | Da specificare | Filtro direzionale |
| 11 | Session Timing | Da specificare | Filtro orario/sessione |
| 12 | Candle Pattern | Da specificare | Solo se oggettivizzabile |
| 13 | [[IDEAS/fft_clock_trigger_hft_filter|FFT Clock Trigger HFT Filter]] | Da specificare | Filtro microstruttura da SSRN 2487656 |
| 14 | [[IDEAS/fft_spectral_regime_filter|FFT Spectral Regime Filter]] | Da specificare | Regime filter spettrale |
| 15 | [[IDEAS/seasonal_ecm_exogenous_signal|Seasonal ECM Exogenous Signal]] | Ricerca statistica | Cointegration per regime |
| 16 | [[IDEAS/momentum_volume_lifecycle|Momentum Volume Lifecycle]] | Da specificare | Momentum/reversal con volume |

## Strategie ideas

- [[IDEAS/fft_trend_following]]
- [[IDEAS/fractal_circular_confluence]]
- [[IDEAS/fractal_fft_pattern_projection]]
- [[IDEAS/atr_channel_breakout]]
- [[IDEAS/fft_clock_trigger_hft_filter]]
- [[IDEAS/fft_spectral_regime_filter]]
- [[IDEAS/seasonal_ecm_exogenous_signal]]
- [[IDEAS/momentum_volume_lifecycle]]

## Classifica robustezza

1. **RSI Mean-Rev** - 77% profittevoli, robusto su tutti i TF
2. **Fractal S/R** - 68% profittevoli, precision entry M1
3. **VWAP Trend** - 68% profittevoli M1, filtro bias giornaliero
4. **Derivate 1/2 ordine** - PF 2.70, forte su M5, momentum puro
5. **FFT Dominant Cycle** - 43% profittevoli M15, London N=256 (nuovo)
6. **EMA Ribbon** - 30% profittevoli M15, filtro direzionale London
7. **BB Squeeze** - 18% profittevoli, usare come filtro regime
8. **ATR Channel Breakout** - 10% profittevoli M15, debole
9. **MA Cross** - 3% profittevoli, solo come regime filter

## Prossimo da testare

-> #12 FFT Spectral Regime Classifier, poi #16 Jump / Spike Filter (vedi [[../../00_CORE/00_Regole_Progettazione]])
| 14 | [[TESTED/14_FFT_Clock_Trigger_HFT_Filter]] | Completato | 1.071 (RSI+clock London) | M15 | RSI NY +0.065 gain · terzo layer filtro clock-driven |
| 17 | [[TESTED/17_FFT_Derivative_Confluence]] | Completato | 1.707 (robust) / 2.083 (best) | M15 | London · DD=7.8% · PRIMA STRATEGIA CHE SUPERA IL TARGET PF>1.3 |
| 18 | [[TESTED/18_Fractal_FFT_Confluence]] | Completato | 1.268 (M5 NY) | M5 | NY+Asian · 1372 trade 5yr · DD 37% · frequenza OK ma DD alta |
