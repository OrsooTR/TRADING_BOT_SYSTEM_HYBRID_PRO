---
title: Momentum Volume Lifecycle
type: strategy_idea
status: backlog
priority: high
source: ssrn-1734526
---

# Momentum Volume Lifecycle

## Ipotesi

Il momentum non ha sempre la stessa qualita. La combinazione tra rendimento e volume identifica la fase del ciclo: accumulo informato, momentum pubblico, distribuzione/reversal, esaurimento.

## Fasi operative

| Fase | Condizione | Azione candidata |
|------|------------|------------------|
| Low volume winner | rendimento positivo, volume sotto media | osservare o entrare con size piccola |
| High volume winner | rendimento positivo, volume crescente | trend-following con trailing stop |
| High volume loser | rendimento debole/negativo, volume alto | cercare reversal o uscire da long |
| Low volume loser | rendimento negativo, volume basso | evitare inseguimento, cercare stabilizzazione |

## Feature

- rendimento rolling;
- accelerazione del rendimento;
- volume z-score;
- volume percentile;
- divergenza prezzo-volume;
- distanza da media/anchored VWAP;
- conferma da derivate `d1` e `d2`.

## Regole candidate

1. Calcolare rendimento rolling su N barre.
2. Calcolare volume z-score su finestra piu lunga.
3. Classificare fase lifecycle.
4. Abilitare trend-following solo in high volume winner con accelerazione non deteriorata.
5. Abilitare reversal solo in high volume loser con `d2` contraria al trend precedente.

## Backtest minimo

- Asset: EURUSD M1/M5/M15 e XAUUSD se disponibile.
- Baseline: momentum semplice.
- Variante: momentum filtrato per volume lifecycle.
- Variante reversal: short/mean-reversion dopo high volume loser.

## Metriche

- PF per fase;
- hit rate dopo transizione fase;
- durata media momentum;
- DD nei falsi continuation;
- stabilita OOS.

## Collegamenti

- [[../../01_THEORY/BEHAVIORAL_FINANCE/ssrn_1734526_entropy_momentum_reversal]]
- [[../../03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]
- [[../../05_METRICS/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
