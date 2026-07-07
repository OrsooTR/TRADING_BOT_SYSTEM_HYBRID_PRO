---
title: FFT + Derivative Confluence
type: strategy_idea
status: da_testare
priority: high
numero: 17
source: compendium_cap_15
---

# 17 — FFT + Derivative Confluence

## Ipotesi
La combinazione di FFT (contesto ciclico) e derivate del primo ordine (timing) è più robusta dei due segnali presi singolarmente. La FFT identifica se il mercato è in una fase ciclica attiva e in quale direzione, la derivata conferma il momento preciso di entrata. È il primo vero setup ibrido multi-layer del sistema.

## Logica operativa
1. FFT dominant cycle (#11): calcolare `cycle_slope` e `dominant_power_ratio`
2. Derivata primo ordine (#02): calcolare `d1` del prezzo smussato
3. Segnale combinato:
   - Long: `cycle_slope > 0` AND `d1 > threshold` AND `dominant_power_ratio > min_quality`
   - Short: `cycle_slope < 0` AND `d1 < -threshold` AND `dominant_power_ratio > min_quality`
4. Entry: next-bar open · SL = sl_mult × ATR · TP = RR × SL

## Livelli di confluenza
| Livello | Condizione | Azione |
|---------|-----------|--------|
| Forte | FFT + d1 concordano, power_ratio alto | Entry full size |
| Medio | Solo FFT o solo d1 | Entry ridotta o skip |
| Assente | Contraddizione | No trade |

## Feature richieste
- Tutti i feature di [[fft_dominant_cycle]] (#11)
- Tutti i feature di [[../TESTED/02_Derivative_1st_2nd_Order]] (#02)
- `confluence_score`: 0 / 1 / 2 (quanti segnali concordano)

## Parametri da gridare
| Parametro | Valori |
|-----------|--------|
| Finestra FFT N | 64, 128 |
| Threshold d1 | 0.0001, 0.0002 |
| min power_ratio | 0.20, 0.30 |
| sl_atr_mult | 1.0, 1.5 |
| RR | 2.0, 3.0 |
| Session | all, london, newyork, asian |
| TF | M5, M15 (M1 opzionale) |

## Backtest minimo
- Train 2020-2023, OOS 2024-2025
- Confronto baseline A: solo Derivate (#02) PF 2.70 M5
- Confronto baseline B: solo FFT (#11)
- Ipotesi: la confluenza riduce i falsi segnali e migliora il DD

## Metriche chiave
- PF vs PF baseline
- DD vs DD baseline
- Riduzione numero trade (= riduzione falsi segnali)
- Stabilità OOS: il `confluence_score` rimane predittivo?

## Rischi noti
- Doppio lag: FFT + derivata entrambe introducono ritardo
- Se i due segnali sono correlati non c'è vera diversificazione
- Overfitting sul threshold del `dominant_power_ratio`

## Note dal compendium (cap. 15)
- FFT → contesto ciclico · Derivata → timing · Frattale → geometria
- Se una sola componente è forte e le altre deboli → trattare con cautela
- Il sistema non deve inseguire precisione assoluta ma ripetibilità dell'edge

## Prerequisiti
- [ ] #11 FFT Dominant Cycle testato e validato
- [x] #02 Derivate 1°/2° ordine testato (PF 2.70 M5)

## Relazione con altri concetti
- Evoluzione naturale verso [[fractal_fft_pattern_projection]] (#18) aggiungendo il layer frattale

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../TESTED/02_Derivative_1st_2nd_Order]]
- [[fft_dominant_cycle]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
