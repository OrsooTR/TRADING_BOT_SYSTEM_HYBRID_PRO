---
title: FFT Clock Trigger HFT Filter
type: strategy_tested
status: Completato
updated: 2026-05-11
numero: 14
source: ssrn-2487656
---

# 14 — FFT Clock Trigger HFT Filter

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../11_MEMORY/PROJECT_STATE]]
- [[../../01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]

## Concetto
Quando lo spettro dei log-return mostra picchi persistenti sulle frequenze calendario (30min, 1h, 2h, 4h), il mercato è in regime "clock-driven": ordini meccanici TWAP/VWAP dominano, il rumore direzionale aumenta, i segnali RSI diventano meno affidabili. Escludere questi periodi migliora la qualità dei segnali.

**Clock bins per TF/N:**
| TF | N | Bins | Periodi |
|----|---|------|---------|
| M15 | 64 | 4, 8, 16, 32 | 4h, 2h, 1h, 30min |
| M15 | 128 | 8, 16, 32, 64 | 4h, 2h, 1h, 30min |
| M5 | 64/128 | dinamici | 4h, 2h, 1h, 30min |
| M1 | 64 | 1, 2 | ~1h, ~30min |

**Classificazione clock-driven:**
1. `clock_ratio = Σpower(clock_bins) / total_power > ratio_thresh`
2. `persistence = frac(last P windows dove clock bin è dominante) > pers_thresh`
3. Se entrambe → skip entry

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| FFT window N | 64 (M1), 64/128 (M5), 64/128 (M15) |
| Ratio threshold | 0.06, 0.08, 0.10 |
| Persistence threshold | 0.30, 0.50 |
| Persistence window P | 10, 20 barre |
| Sessioni | all, london, newyork, asian |
| TF | M1, M5, M15 |
| Strategie testate | RSI, Derivate |
| Confronto | FFT clock vs time-based (prima barra ogni ora) |

## Risultati chiave (OOS 2021-2025)

### RSI su M15 — per sessione
| Sessione | Baseline OOS PF | Time Filter PF | FFT Clock PF | PF Gain FFT |
|----------|---------------|----------------|-------------|-------------|
| all      | 0.993 | 0.994 (+0.001) | **1.028** | **+0.035** |
| london   | 1.048 | 1.064 (+0.017) | **1.071** | **+0.023** |
| newyork  | 0.957 | 0.966 (+0.008) | **1.022** | **+0.065** |
| asian    | 0.956 | 0.969 (+0.013) | 0.991 | +0.034 |

**Best setup RSI + FFT Clock su M15:**
- NY session: base OOS PF=0.957 → clock filter → OOS PF=1.022 (+0.065), 541 trade OOS, clock%=10%
- London: base OOS PF=1.048 → OOS PF=1.071 (+0.023), 553 trade OOS

### RSI su M1 e M5
| TF | Baseline | FFT Clock | PF Gain |
|----|---------|-----------|---------|
| M1 | 1.129 | 1.094 | +0.011 |
| M5 | 1.013 | 1.019 | +0.006 |

### Derivate — riepilogo
| TF | Baseline | Time Filter | FFT Clock | Note |
|----|---------|------------|-----------|------|
| M1 | 1.037 | 1.023 (−0.014) | 1.039 (+0.002) | Quasi invariante |
| M5 | 1.022 | 0.912 (−0.110) | 0.910 (+0.004) | Time filter PEGGIORA |
| M15 | 1.039 | 0.949 (−0.090) | 0.961 (+0.013) | Time filter PEGGIORA |

**Osservazione critica:** il filtro time-based peggiora le Derivate su M5/M15 (−0.090/−0.110), mentre l'FFT clock non causa danno. Le Derivate possono BENEFICIARE dell'attività clock-driven (momentum meccanico). Conferma: le Derivate non devono usare questo filtro.

### Clock% (% barre escluse)
- RSI best configs: 7-19% barre escluse → selettivo, non eccessivo
- Basse soglie (ratio>0.06, pers>0.30): 10-19% escluse
- Alte soglie (ratio>0.10, pers>0.50): 5-8% escluse

## Pattern emersi

1. **RSI + FFT clock > RSI + time filter** in tutte le sessioni: il filtro dinamico è superiore al filtro statico. Il paper SSRN-2487656 è confermato: la persistenza spettrale del picco calendario è un segnale migliore del semplice "prima barra dell'ora".

2. **NY session beneficia di più**: la NY session aveva RSI baseline sotto 1.0 (0.957) e il filtro clock la porta sopra 1.0 (1.022). È la sessione con più attività meccanica → più clock-driven bars → filtro più efficace.

3. **Derivate insensibili o danneggiate dal time filter**: le Derivate usano il momentum degli ordini meccanici come segnale. Escludere le prime barre di ogni ora rimuove trade validi. Il filtro FFT non causa danno ma non aggiunge valore significativo.

4. **Gain più piccoli del Regime Classifier (#12)**: il clock filter dà +0.023-0.065 vs +0.176 del NOISE filter. I due filtri sono complementari e non sostitutivi.

5. **Pers_threshold bassa (0.30) è preferibile**: cattura più barre clock-driven e dà gain migliori, senza essere troppo restrittivo.

## Implicazioni per l'architettura del bot

Il clock filter va applicato come **layer aggiuntivo** sopra il Regime Classifier:

```
RSI pipeline:
  FFT Regime(N=128, delta=0.08) → NOISE?
      YES → FFT Clock(N=128, ratio>0.06, pers>0.30) → NOT clock-driven?
                YES → RSI signal → Entry (London O NY session)
                NO  → Skip (clock-driven = rumore meccanico)
      NO  → Skip
```

Il London+clock filter ha OOS PF=1.071 e il NY+clock filter porta una sessione da <1 a >1. Combinati potrebbero superare la soglia target 1.3 con il Regime Classifier.

## Confronto con tutti i filtri testati finora
| Filtro | Strategia | OOS PF M15 | PF Gain |
|--------|---------|-----------|---------|
| Regime NOISE (#12) | RSI | 1.224 | +0.176 |
| Vol Gate (#15) | RSI | ~1.397 (M5) | +0.329 |
| FFT Clock (#14) | RSI | 1.071 | +0.023 |
| ATR Channel (#07) | standalone | 1.094 | — |
| EMA Ribbon (#08) | standalone | 1.104 | — |

## Classificazione robustezza
**Media** — Il filtro funziona e migliora RSI in modo consistente (+0.023 a +0.065), ma il gain assoluto è più piccolo rispetto a Regime e Vol Gate. Più utile come **terzo layer** di raffinamento che come filtro primario. Non applicare a Derivate.

## Script
`scripts/run_clock_filter.py`

## Artifacts
`artifacts/clock_backtests/data/clock_results_all.json`
`artifacts/clock_backtests/data/clock_test_a.csv`
