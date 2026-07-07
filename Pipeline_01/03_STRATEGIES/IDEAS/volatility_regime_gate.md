---
title: Volatility Regime Gate
type: strategy_idea
status: testato
priority: medium
numero: 15
source: compendium_cap_16_17
---

# 15 — Volatility Regime Gate

## Ipotesi
Il livello relativo di volatilità (ATR percentile su finestra lunga) determina quale famiglia di strategie ha edge: bassa volatilità → mean reversion (RSI, VWAP); alta volatilità → breakout/momentum (Derivate, ATR Channel). Testarlo come meta-filtro binario applicato alle strategie già validate.

## Logica operativa
1. Calcolare `atr_pct = percentile_rank(ATR_14, finestra_lunga)` su ogni barra
2. Classificare: `atr_pct < soglia_bassa` → regime bassa vol; `atr_pct > soglia_alta` → regime alta vol
3. Applicare solo la strategia appropriata per il regime attivo
4. Zona grigia (tra le due soglie): no trade o size ridotta

## Feature
- `atr_percentile`: percentile rank dell'ATR corrente su finestra rolling L
- `vol_regime`: low / mid / high
- `vol_trend`: in espansione o contrazione (derivata dell'ATR)

## Parametri da gridare
| Parametro | Valori |
|-----------|--------|
| Finestra percentile L | 50, 100, 200 barre |
| Soglia bassa vol | 20°, 30° percentile |
| Soglia alta vol | 70°, 80° percentile |
| Strategia in bassa vol | RSI MeanRev, VWAP |
| Strategia in alta vol | Derivate, ATR Channel |
| TF | M1, M5, M15 |

## Backtest minimo
- Non un backtest standalone: va testato applicato a una strategia esistente
- Test A: RSI (#03) solo quando `vol_regime = low` → PF migliora?
- Test B: Derivate (#02) solo quando `vol_regime = high` → DD si riduce?
- Confronto: strategia con gate vs strategia senza gate

## Metriche chiave
- Delta PF: (PF con gate) - (PF senza gate)
- Riduzione trades: quanti trade elimina il gate?
- Stabilità OOS: il regime classificato correttamente in OOS?

## Rischi noti
- Overfitting sulle soglie: usare valori rotondi, non ottimizzati
- La volatilità cambia regime lentamente → lag nella classificazione
- Finestre brevi: troppo reattivo. Finestre lunghe: troppo lento.

## Note dal compendium (cap. 16-17)
- Il regime cambia il tipo di strumento necessario, non solo l'intensità
- La classificazione non deve essere binaria: zona grigia = no trade
- Il rischio va definito prima del profitto, non dopo

## Relazione con altri concetti
- Si combina con quasi tutte le strategie testate
- Prerequisito naturale per [[fft_spectral_regime_filter]] (#12) che fa la stessa cosa via spettro FFT
- Versione semplice (ATR-based) da validare prima della versione FFT

## Stato attuale
- Backtest completato il 2026-05-08
- Vedi nota testata: [[../TESTED/15_Volatility_Regime_Gate]]

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../TESTED/03_RSI_MeanReversion]]
- [[../TESTED/02_Derivative_1st_2nd_Order]]
- [[../TESTED/15_Volatility_Regime_Gate]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
