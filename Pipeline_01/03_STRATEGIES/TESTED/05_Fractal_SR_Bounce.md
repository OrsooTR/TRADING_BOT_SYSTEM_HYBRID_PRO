# 05 — Fractal Support & Resistance Bounce

## Collegamenti
- [[../INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../04_BACKTEST/INDEX]]
- [[../../05_METRICS/INDEX]]
- [[../../09_LOGS/report_giornata_2026-04-28]]
- [[01_MA_Crossover]]
- [[02_Derivative_1st_2nd_Order]]
- [[03_RSI_MeanReversion]]
- [[04_BB_Squeeze]]
- [[../../14_COMPENDIUM/06_Frattali]]

## Concetto
I frattali di Williams identificano massimi e minimi locali su una finestra di barre.
- **Pivot High**: h[i] = massimo nella finestra [i-fp, i+fp] → livello di **resistenza**
- **Pivot Low**: l[i] = minimo nella finestra [i-fp, i+fp] → livello di **supporto**
- Il **bounce** si verifica quando il prezzo si avvicina al livello e rimbalza nella direzione opposta

## Logica operativa
1. Calcola frattali rolling con shift di fp barre (no look-ahead bias)
2. Cerca i livelli attivi nell'ultima finestra `lookback` barre
3. Trova il supporto e la resistenza più vicini al prezzo corrente
4. Se `|close - support| ≤ tol×ATR` e `close ≥ support` → LONG (bounce da supporto)
5. Se `|close - resistance| ≤ tol×ATR` e `close ≤ resistance` → SHORT (bounce da resistenza)

## Entry rules
| Direzione | Condizione |
|-----------|-----------|
| LONG | dist(close, nearest_support) ≤ tol×ATR AND close ≥ support (tocca da sopra) |
| SHORT | dist(close, nearest_resistance) ≤ tol×ATR AND close ≤ resistance (tocca da sotto) |

## Risk model
- SL = 1.5 × ATR(14)
- TP = SL × RR
- Range RR testato: 2:1, 3:1, 4:1

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| Fractal Period (fp) | 2, 3, 5 |
| Tolerance (tol) | 0.3, 0.5, 1.0, 1.5 × ATR |
| Lookback (lb) | 30, 70 barre |
| RR | 2:1, 3:1, 4:1 |
| TF | M1, M5, M15 |
| Simbolo | EURUSD |
| Periodo | 2020-2025 (subset) |

## Totale test: 216

## Risultati
### Profittabilità per TF
| TF | Test | Profittevoli | % | Best PF |
|----|------|-------------|---|---------|
| M1 | 72 | 70 | **97%** | 1.18 |
| M5 | 72 | 65 | **90%** | 1.07 |
| M15 | 72 | 11 | **15%** | 1.03 |

### Top 5
| TF | fp | tol | lb | RR | Trades | WR | PF |
|----|-----|-----|-----|-----|--------|-----|-----|
| M1 | 5 | 0.3 | 30 | 3:1 | 3647 | 28% | **1.18** |
| M1 | 5 | 1.5 | 30 | 3:1 | 4572 | 28% | **1.16** |
| M1 | 5 | 1.0 | 30 | 3:1 | 4431 | 28% | **1.16** |
| M1 | 5 | 0.5 | 30 | 3:1 | 4067 | 28% | **1.15** |
| M1 | 5 | 0.3 | 30 | 2:1 | 4733 | 36% | **1.13** |

## Pattern emersi
1. **M1 97% profittevole** — il concetto funziona molto bene a bassa granularità
2. **Fractal period=5** domina: finestra più ampia filtra i pivot minori (meno falsi livelli)
3. **Lookback=30** migliore su M1: livelli recenti più rilevanti, non storici stantii
4. **RR=3:1 sweet spot**: WR 28% compensato da vincite triple
5. **Tolleranza 0.3-0.5 ATR**: touch precisi evitano falsi bounce su livelli "a distanza"
6. **M15 quasi inutile**: la struttura frattale M15 non offre edge di bounce

## Confronto con altri concetti
| Metrica | MA Cross | Derivate | RSI | BB Squeeze | **Fractal S/R** |
|---------|----------|----------|-----|------------|-----------------|
| % profittevoli | 3% | 12% | **77%** | 18% | **68%** |
| Best PF | 1.13 | **2.70** | 1.59 | 1.22 | 1.18 |
| TF ideale | M1 | M5 | M1 | M15 | M1 |
| Robustezza | Bassa | Media | **Alta** | Bassa | **Alta** |

## Lezione per il bot finale
> Fractal S/R ha edge robusto (68% test profittevoli, 2° solo a RSI).
> I livelli frattali come support/resistance sono punti naturali di reazione del prezzo.
> Uso ideale nel bot: livelli frattali come **zone di entry precision** per i segnali FFT.
> Quando FFT predice rimbalzo E il prezzo è su un livello frattale → alta conviction.
> fp=5 + lb=30 + RR=3 = configurazione ottimale per M1.

## Stato
- [x] Backtest grid search completato (216 test)
- [x] Fogli Excel aggiunti (FRAC_SUMMARY, FRAC_ALL, FRAC_M1/M5/M15)
- [x] Grafici gaussiani aggiunti in GAUSSIAN_ANALYSIS
- [x] Scheda strategia aggiunta in STRATEGY_DESCRIPTIONS
- [x] Vault Obsidian aggiornato
