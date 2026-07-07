---
title: Experiment Protocol
type: project_memory
priority: high
updated: 2026-04-22
---

# Experiment Protocol

## Collegamenti
- [[INDEX]]
- [[PROJECT_STATE]]
- [[../04_BACKTEST/INDEX]]
- [[../05_METRICS/INDEX]]
- [[../09_LOGS/esperimenti]]

## Obiettivo
Standardizzare come vengono registrati i test per mantenere il progetto leggibile e confrontabile.

## Ogni esperimento dovrebbe includere
- nome del concetto
- asset
- timeframe
- periodo dati
- ipotesi da testare
- parametri
- logica entry
- logica exit
- risk model
- split train/test
- metriche principali
- risultato finale
- decisione successiva

## Metriche minime da riportare
- profit factor
- drawdown
- winrate
- numero trade
- profitto netto o rendimento percentuale
- degradazione OOS, se disponibile

## Decisione finale ammessa
- promote
- hold
- reject
- retest

## Naming suggerito
- `test_[concept]_[asset]_[tf]_[date].md`
- `retest_[concept]_[asset]_[tf]_[date].md`

## Regola pratica
Se un test non e riproducibile o manca il contesto dei parametri, non vale come memoria utile.
