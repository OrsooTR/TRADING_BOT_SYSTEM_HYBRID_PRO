---
title: Jump / Spike Filter
type: strategy_idea
status: da_testare
priority: low
numero: 16
source: compendium_cap_23_24
---

# 16 — Jump / Spike Filter

## Ipotesi
Le barre con rendimento > N × ATR sono eventi di salto Merton-style (shock macro, news, liquidità). Includerle nel backtest distorce le metriche e include trade non eseguibili in live (gap, slippage estremo). Escluderle dal campione migliora la robustezza delle altre strategie.

## Logica operativa
Questo non è un segnale di entrata ma un filtro di protezione:
1. Calcolare `jump_size = abs(log_return) / ATR_14`
2. Se `jump_size > soglia_jump` → barra classificata come "jump"
3. Opzioni di gestione:
   - A) Non aprire nuovi trade nelle N barre successive al jump
   - B) Escludere completamente le barre jump dal backtest
   - C) Ridurre size nelle N barre successive

## Feature
- `jump_size`: rendimento normalizzato per ATR
- `is_jump`: bool, se supera la soglia
- `bars_since_jump`: quante barre dall'ultimo jump
- `jump_frequency`: frequenza di jump nel periodo (contesto di regime)

## Parametri da testare
| Parametro | Valori |
|-----------|--------|
| Soglia jump (× ATR) | 2.5, 3.0, 4.0 |
| Cooldown post-jump (barre) | 0, 1, 3 |
| Modalità | esclusione vs cooldown vs size ridotta |
| TF | M1, M5, M15 |

## Backtest minimo
- Non standalone: applicare come filtro alle strategie già testate
- Misurare: quante barre vengono escluse? Come cambia il PF?
- Verificare: i jump si concentrano in specifiche ore/sessioni?

## Metriche chiave
- % barre classificate come jump per TF
- Variazione PF con e senza filtro
- Distribuzione jump per ora del giorno e per anno

## Rischi noti
- Se troppi trade vengono esclusi → perdita di edge statistico
- La soglia ottimale varia con il regime: in alta volatilità i "jump normali" aumentano
- Non tutti i gap su M1 sono jump reali: alcuni sono apertura barre dopo weekend

## Note dal compendium (cap. 23-24)
- I salti sono coerenti con shock macro, news improvvise e accelerazioni di liquidità
- La presenza di salti cambia la coda della distribuzione → SL standard può essere inadeguato
- Variance Gamma e Lévy: il mercato non va ridotto a una sola forma di rumore
- Il bot deve essere compatibile con distribuzioni non gaussiane

## Relazione con altri concetti
- Da applicare su #02 (Derivate), #03 (RSI), #07 (Fractal) come primo test
- Complementare al [[volatility_regime_gate]] (#15): vol alta non è uguale a jump

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../TESTED/02_Derivative_1st_2nd_Order]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
