---
title: Walk-Forward Validation Engine
type: research_idea
priority: high
created: 2026-07-07
---

# 12 - Walk-Forward Validation Engine

## Collegamenti
- [[INDEX]]
- [[../DEVELOPMENT_BACKLOG]]
- [[../../04_BACKTEST/INDEX]]

## Ipotesi
Lo split fisso Train 2020 / OOS 2021-2025 seleziona parametri su un solo anno (per di più
l'anno COVID, atipico). Un motore walk-forward — es. finestre rolling 12 mesi train / 3 mesi
test, riottimizzando ad ogni passo — misura la **stabilità temporale** dell'edge, non solo la
sua esistenza media.

## Cosa costruire
1. Wrapper generico `walk_forward(grid_fn, df, train_months=12, test_months=3)` che riusa
   gli stessi `sim_and_metrics` dei runner esistenti.
2. Metriche di uscita: PF medio dei periodi test, % di periodi test profittevoli,
   dispersione dei parametri ottimi tra le finestre.
3. Criterio: un setup è promosso solo se profittevole in >60% delle finestre test.

## Perché è prioritaria
È già richiesta dalla FFT implementation checklist ("walk-forward o stabilità per finestra
prima della promozione finale") ma non esiste ancora nel codice.

## Effort stimato
Medio: il motore vettoriale è già veloce (una grid completa gira in minuti), quindi
ripeterla su ~20 finestre è fattibile.
