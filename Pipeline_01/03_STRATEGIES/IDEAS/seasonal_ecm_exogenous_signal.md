---
title: Seasonal ECM Exogenous Signal
type: strategy_idea
status: backlog
priority: medium
source: ssrn-2487656
---

# Seasonal ECM Exogenous Signal

## Ipotesi

Una variabile esogena puo essere utile solo se testata nel regime corretto. Il paper su NG futures mostra che la cointegration prezzo-temperatura fallisce sul campione aggregato, ma diventa significativa quando il campione viene diviso per stagioni.

## Applicazione nel nostro progetto

Per EURUSD e XAUUSD la variabile esogena non sara temperatura, ma il principio resta utile:

- EURUSD: DXY, yield spread, calendario macro, volatilita implicita FX.
- XAUUSD: real yields, DXY, VIX, tassi USA, calendario CPI/FOMC.
- Commodities: meteo, scorte, stagionalita fisica.

## Feature

- spread tra prezzo e valore ECM stimato;
- z-score dello spread;
- regime stagionale/sessione;
- errore di previsione della variabile esogena;
- velocita di convergenza verso equilibrio.

## Regole candidate

1. Dividere il campione per regime: stagione, sessione, macro regime o volatilita.
2. Testare cointegration tra prezzo e variabile esogena per ogni regime.
3. Accettare solo regimi con p-value sotto soglia e stabilita OOS.
4. Entrare mean-reversion quando lo spread prezzo-equilibrio supera soglia.
5. Evitare il segnale quando il regime non passa il test.

## Backtest minimo

- Prima fase: solo ricerca statistica, senza trading.
- Seconda fase: spread mean-reversion con stop temporale.
- Terza fase: integrazione come filtro del decision engine.

## Rischi

- Data snooping nella scelta delle stagioni.
- Variabili esogene non disponibili in tempo reale.
- Cointegration instabile su campioni brevi.

## Collegamenti

- [[../../01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]
- [[../../02_DATA/INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
