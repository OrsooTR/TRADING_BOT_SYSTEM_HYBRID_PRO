---
title: Monte Carlo Bootstrap dei trade
type: research_idea
priority: medium
created: 2026-07-07
---

# 14 - Monte Carlo Bootstrap dei trade

## Collegamenti
- [[INDEX]]
- [[../../05_METRICS/INDEX]]
- [[10_failure_database]]

## Ipotesi
PF e max drawdown di un singolo backtest sono UNA realizzazione di un processo aleatorio.
Ricampionando i trade (bootstrap con reimmissione, o shuffle dell'ordine) 1000+ volte si
ottiene la **distribuzione** di PF e DD, non un numero solo.

## Cosa costruire
1. `monte_carlo(pnl_r, n=1000)` → distribuzione di PF, DD, equity finale.
2. Metriche decisionali: PF al 5° percentile (worst case realistico), probabilità di
   DD > 12% (la soglia delle Regole di Progettazione), probabilità di rovina.
3. Criterio di promozione aggiuntivo: `P(PF > 1) >= 90%` sul bootstrap OOS.

## Applicazione
I simulatori vettoriali producono già l'array `pnl_r` per ogni combo: basta salvare i
pnl_r del best setup ed eseguire il bootstrap come step finale del runner.

## Effort stimato
Basso: ~50 righe di numpy, nessun dato nuovo necessario.
