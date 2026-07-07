---
title: FFT Clock Trigger HFT Filter
type: strategy_idea
status: da_testare
priority: high
numero: 14
source: ssrn-2487656
---

# FFT Clock Trigger HFT Filter

## Ipotesi

Se il mercato mostra una componente spettrale forte e persistente su frequenze meccaniche, come minuto, ora, apertura o chiusura, il segnale direzionale diventa piu fragile. In quei regimi conviene ridurre size, filtrare entry o evitare trade di breakout immediati.

## Feature

- potenza FFT sulla frequenza target;
- rapporto tra potenza target e media delle frequenze vicine;
- stabilita del picco su finestre rolling;
- eventuale concentrazione volume nei primi secondi, se disponibili dati tick/second-level.

## Regole candidate

1. Calcolare spettro rolling su prezzo o rendimento.
2. Identificare picchi su frequenze calendario: minuto, ora, sessione, giorno.
3. Se `peak_strength > soglia` e `peak_persistence > soglia`, marcare regime clock-driven.
4. In regime clock-driven:
   - ridurre size;
   - evitare entry nei primi minuti della sessione;
   - richiedere conferma da trend/derivate;
   - testare uscita piu rapida.

## Backtest minimo

- Dataset: EURUSD M1, XAUUSD M1, eventuale NG/commodity se disponibile.
- Train/test: rolling walk-forward.
- Confronto: strategia base vs strategia con filtro clock-driven.
- Metriche: PF, DD, trade/anno, OOS degradation, turnover, slippage sensitivity.

## Rischi

- Con OHLC M1 non si vede il primo secondo del minuto.
- Il picco puo descrivere microstruttura, non direzione.
- Frequenze calendario possono essere aliasing o effetto sessione.

## Collegamenti

- [[../../01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]
- [[fft_trend_following]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
