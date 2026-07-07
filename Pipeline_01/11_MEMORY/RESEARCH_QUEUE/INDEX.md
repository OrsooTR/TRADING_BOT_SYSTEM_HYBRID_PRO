---
title: Research Queue Index
type: project_research_queue
priority: medium
---

# Research Queue Index

Questa cartella raccoglie le ipotesi di ricerca, le idee sperimentali e i moduli tecnici da valutare nel tempo.

## Ordine di lavoro consigliato
1. Adaptive ATR
2. Wavelet Transform
3. Hurst Exponent
4. Volatility Clustering
5. Hilbert Transform
6. Kalman Filter
7. Entropy Filters
8. Phase Synchronization
9. Market Microstructure
10. Failure Database
11. Experiment Template
12. Walk-Forward Validation (prioritaria: richiesta dalla checklist FFT)
13. Parameter Stability Score (anti-overfitting, costo zero sui CSV esistenti)
14. Monte Carlo Bootstrap dei trade

## Relazione con la pipeline
- Le idee operative e le ipotesi future vivono qui.
- Le decisioni definitive vanno in `11_MEMORY/DECISIONS_LOG.md`.
- Gli esperimenti eseguiti vanno in `09_LOGS`.
- I moduli stabili passano in `03_STRATEGIES/TESTED` o nelle sezioni tecniche corrette.

## File
- [[01_wavelet_transform]]
- [[02_hilbert_transform]]
- [[03_entropy_filters]]
- [[04_hurst_exponent]]
- [[05_adaptive_atr]]
- [[06_volatility_clustering]]
- [[07_phase_synchronization]]
- [[08_kalman_filter]]
- [[09_market_microstructure]]
- [[10_failure_database]]
- [[11_experiment_template]]
- [[12_walk_forward_validation]]
- [[13_parameter_stability_score]]
- [[14_monte_carlo_bootstrap]]
