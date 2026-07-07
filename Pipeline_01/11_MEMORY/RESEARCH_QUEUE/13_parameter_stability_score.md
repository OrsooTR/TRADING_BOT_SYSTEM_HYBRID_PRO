---
title: Parameter Stability Score
type: research_idea
priority: high
created: 2026-07-07
---

# 13 - Parameter Stability Score (anti-overfitting)

## Collegamenti
- [[INDEX]]
- [[12_walk_forward_validation]]
- [[../../00_CORE/00_Regole_Progettazione]]

## Ipotesi
Nelle grid search il "best setup" per PF è spesso un picco isolato (overfitting).
Un setup robusto vive su un **plateau**: i vicini nel param-space hanno PF simile.

## Cosa costruire
Per ogni combinazione della griglia calcolare uno stability score:
`stability = median(PF dei vicini a distanza 1 in ogni parametro) / PF proprio`
- score ≈ 1 → plateau, robusto
- score << 1 → picco isolato, sospetto

Poi ordinare i risultati per `PF_penalizzato = PF * min(stability, 1)` invece che per PF puro.

## Applicazione immediata
Ricalcolo a costo zero: i CSV dei risultati contengono già tutta la griglia — si può
implementare come post-processing in `scripts/` e mostrare lo score sulla dashboard
(tab Ottimizzazione) accanto a ogni combinazione.

## Nota
La dashboard mostra già gli scatter PF-vs-parametro: i plateau sono visibili a occhio,
questo score li rende quantitativi e ordinabili.
