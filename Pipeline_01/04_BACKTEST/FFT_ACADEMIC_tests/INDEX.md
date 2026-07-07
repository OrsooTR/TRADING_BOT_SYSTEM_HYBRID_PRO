---
title: FFT Academic Tests Index
type: backtest_index
priority: high
---

# FFT Academic Tests Index

## Scopo

Trasformare le fonti accademiche importate in test riproducibili.

## Test 01 - Clock-trigger filter

Strategia: [[../../03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

Domanda: un regime con picchi spettrali meccanici peggiora le strategie trend/momentum?

Output minimo:

- `peak_strength`
- `peak_persistence`
- regime `clock_driven`
- confronto strategia base vs strategia filtrata

## Test 02 - Spectral regime filter

Strategia: [[../../03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]

Domanda: la distribuzione della potenza FFT separa regimi trend e regimi noise?

Output minimo:

- `low_freq_power`
- `high_freq_power`
- `hf_ratio`
- `spectral_slope`
- PF/DD per regime

## Test 03 - Seasonal ECM exogenous signal

Strategia: [[../../03_STRATEGIES/IDEAS/seasonal_ecm_exogenous_signal]]

Domanda: una variabile esogena diventa utile solo dopo split per regime?

Output minimo:

- test cointegration per regime;
- spread prezzo-equilibrio;
- z-score spread;
- stabilita OOS.

## Test 04 - Momentum volume lifecycle

Strategia: [[../../03_STRATEGIES/IDEAS/momentum_volume_lifecycle]]

Domanda: volume e accelerazione distinguono momentum continuativo da reversal?

Output minimo:

- classificazione fase;
- rendimento futuro per fase;
- PF di baseline momentum vs lifecycle filter;
- distribuzione DD per fase.

## Collegamenti

- [[../INDEX]]
- [[../../01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]
- [[../../01_THEORY/BEHAVIORAL_FINANCE/ssrn_1734526_entropy_momentum_reversal]]
- [[../../00_CORE/00_Regole_Progettazione]]
