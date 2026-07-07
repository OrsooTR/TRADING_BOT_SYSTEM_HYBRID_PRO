---
title: Report giornata 2026-07-07
type: log
priority: high
---

# Report giornata — 2026-07-07

Giornata di consolidamento infrastrutturale e rigenerazione completa dei backtest.

## Collegamenti
- [[code_review_2026-07-07]]
- [[../11_MEMORY/PROJECT_STATE]]
- [[../11_MEMORY/RESEARCH_QUEUE/INDEX]]

## Cosa è successo
1. **Code review completa** → 7 bug ad alta severità corretti (vedi [[code_review_2026-07-07]]).
2. **Motore vettoriale reso realistico**: tie-break TP/SL pessimistico, spread 0.5 pip,
   chiusura mark-to-market dei timeout, sessioni corrette per fuso EST.
3. **Repo GitHub + dashboard** su Pages con confronto strategie e scatter di ottimizzazione.
4. **Rigenerate le 8 famiglie vettoriali** col motore corretto (Derivative full, VWAP e
   FFT Clock Filter grid restano da rilanciare: motore backtrader, ore di calcolo).
5. CI con smoke test del motore; 3 nuove idee in RESEARCH_QUEUE (#12 walk-forward,
   #13 stability score, #14 Monte Carlo bootstrap).

## Vecchi numeri (gonfiati) vs nuovi (onesti), best setup OOS

| Famiglia | Prima | Dopo | Lettura |
|---|---|---|---|
| ATR Channel | 1.09 | **0.99** (M15) | morta standalone, resta regime filter |
| EMA Ribbon | 1.13 | **0.999** (M15) | morta standalone |
| FFT Cycle | 1.17 | **1.10** (M15) | sopravvive debole, solo M15 |
| FFT Clock su RSI | — | **0.94** (+0.04) | filtro debole |
| Fractal FFT (M5 full) | 1.27 | **0.94** (+0.10 vs base) | sotto 1 coi costi |
| Regime: RSI + noise | — | **1.22** (M15, +0.20 vs base, DD 19%) | ✅ filtro valido |
| Volatility Gate RSI low-vol | +0.33 dPF | **+1.30 (M1) / +2.78 (M15) dPF** | ✅ forte |
| **Confluence #17 (FFT+Derivate)** | — | **2.19 (M15), DD 5.2%, 45 trade** | ✅ il migliore |

Baseline pure (RSI, Derivate) su M1/M5: tutte sotto PF 1 coi costi.

## Lettura strategica
1. **Nessuna entry standalone sopravvive allo spread su M1/M5.** L'edge del progetto non è
   nelle entry, è nei **filtri di contesto su M15** — esattamente la tesi del compendium.
2. La pipeline `Regime (FFT) -> Entry -> Conviction` è confermata dai numeri onesti:
   baseline 0.95 → +FFT cycle 1.88 → +confluence completa 2.19 (M15).
3. **Problema aperto**: la confluence genera ~9 trade/anno, sotto il criterio >50/anno.
   Prossimo lavoro: allargare i trigger (soglie meno strette), unire più setup di plateau
   (vedi [[../11_MEMORY/RESEARCH_QUEUE/13_parameter_stability_score]]) o portafoglio
   multi-timeframe/multi-coppia.
4. Ogni numero va confermato con walk-forward
   ([[../11_MEMORY/RESEARCH_QUEUE/12_walk_forward_validation]]) prima della promozione.

## Prossimi passi concreti
1. Walk-forward sul best setup della confluence #17 e del gate #15.
2. Parameter stability score come post-processing dei CSV esistenti.
3. Rilanciare le famiglie backtrader (Derivative full, VWAP) col fix sessioni.
4. Aggiornare le note TESTED con i numeri onesti (oggi restano storiche).
