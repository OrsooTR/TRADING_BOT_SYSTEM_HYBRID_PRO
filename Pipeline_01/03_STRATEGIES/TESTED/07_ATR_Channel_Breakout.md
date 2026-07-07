---
title: ATR Channel Breakout
type: strategy_tested
status: Completato
updated: 2026-05-07
numero: 05
---

# 07 — ATR Channel Breakout

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]

## Concetto
Canale dinamico: `EMA(period) ± atr_channel_mult × ATR(14)`. Breakout della banda superiore = long, banda inferiore = short. Entry sul prossimo bar open, SL = sl_atr_mult × ATR, TP = RR × SL.

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
EMA: 20/50/100 · ATR mult: 1.5/2.0/2.5/3.0 · SL mult: 1.0/1.5 · RR: 2/3/4 · Sessioni: all/london/newyork/asian · TF: M1/M5/M15 · Totale: 864 combos

## Risultati chiave (OOS 2021-2025, 5 anni)

### Best per sessione su M15
| Sessione | OOS PF | OOS DD% | Config |
|----------|--------|---------|--------|
| asian    | 1.094 | 64.1 | EMA=20, ATR=2.5, SL=1.5, RR=4 |
| london   | 1.019 | 62.9 | — |
| newyork  | 0.975 | 57.1 | — |
| all      | 0.977 | 91.3 | — |

### Profittevoli per TF (OOS PF > 1.0)
| TF | % profittevoli |
|----|---------------|
| M1  | 16% |
| M5  | 8%  |
| M15 | 7%  |

## Lezione
Edge molto debole su 5 anni OOS. La DD è sistematicamente > 60% su M15. Non utilizzabile standalone né come filtro. **Da declassare: non candidato per il bot finale.**

## Classificazione robustezza
**Debole** — peggiorata su OOS lungo. 7% profittevoli M15.

## Script
`scripts/run_atr_vectorized.py`
