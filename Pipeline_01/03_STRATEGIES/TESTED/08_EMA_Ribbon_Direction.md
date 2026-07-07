---
title: EMA Ribbon Direction Filter
type: strategy_tested
status: Completato
updated: 2026-05-07
numero: 08
---

# 08 — EMA Ribbon Direction Filter

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]

## Concetto
Tre EMA (fast/mid/slow). Segnale al momento in cui il ribbon si allinea completamente: bullish (fast>mid>slow) o bearish (fast<mid<slow). Entry next-bar open, SL = sl_mult × ATR(14), TP = RR × SL.

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
Fast: 5/8/13 · Mid: 21/34 · Slow: 55/89 · SL mult: 1.0/1.5 · RR: 2/3/4 · Sessioni: all/london/newyork/asian · TF: M1/M5/M15 · Totale: 864 combos

## Risultati chiave (OOS 2021-2025, 5 anni)

### Top 3 su M15
| Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% |
|------|-----|------|----|----|---------|---------|--------|---------|
| 13 | 21 | 89 | 1.0 | 3.0 | asian | 1.147 | 1.104 | 30.8 |
| 13 | 34 | 55 | 1.0 | 2.0 | asian | 1.083 | 1.102 | 33.3 |
| 5  | 34 | 55 | 1.0 | 3.0 | asian | 1.151 | 1.091 | 33.7 |

### Best per sessione su M15
| Sessione | OOS PF | OOS DD% |
|----------|--------|---------|
| asian    | 1.104 | 30.8 |
| london   | 1.056 | 46.0 |
| all      | 1.022 | 52.4 |
| newyork  | 0.948 | 38.4 |

### Profittevoli per TF (OOS PF > 1.0)
| TF | % profittevoli |
|----|---------------|
| M1  | 41% |
| M5  | 25% |
| M15 | 33% |

## Confronto con split precedente (4yr train / 2yr OOS)
Con il vecchio split la sessione London dominava (PF 1.196). Su 5 anni OOS la **sessione Asian** prende il sopravvento (PF 1.104 vs London 1.056). Questo suggerisce che l'edge London era parzialmente specifico al periodo 2024-2025.

## Lezione
Edge presente ma DD > 30% rende difficile l'uso standalone. Con 5 anni OOS la robustezza si riduce rispetto al vecchio split — normale. Utile come **filtro direzionale** ma non come entry signal autonomo.

## Classificazione robustezza
**Media** — 33% profittevoli M15 su 5 anni OOS. Candidato come filtro regime.

## Script
`scripts/run_ribbon_vectorized.py`
