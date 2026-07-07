# 04 — Bollinger Band Squeeze + Breakout

## Collegamenti
- [[../INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../04_BACKTEST/INDEX]]
- [[../../05_METRICS/INDEX]]
- [[../../09_LOGS/report_giornata_2026-04-28]]
- [[01_MA_Crossover]]
- [[02_Derivative_1st_2nd_Order]]
- [[03_RSI_MeanReversion]]

## Concetto
Le Bande di Bollinger misurano la volatilità tramite deviazione standard mobile.
- **Squeeze** = bandwidth (upper-lower)/mid scende sotto una soglia → mercato compresso
- **Breakout** = primo bar fuori dalla compressione che rompe la banda → segnale direzionale

## Logica operativa
1. Calcola BB(period, std_dev)
2. Calcola bandwidth = (upper - lower) / mid
3. Squeeze = bandwidth ≤ percentile della bandwidth su finestra storica
4. Trigger entry: barra precedente in squeeze + barra corrente fuori squeeze + breakout banda

## Entry rules
| Direzione | Condizione |
|-----------|-----------|
| LONG | prev_bar in squeeze AND cur_bar non in squeeze AND close > upper_band |
| SHORT | prev_bar in squeeze AND cur_bar non in squeeze AND close < lower_band |

## Risk model
- SL = 1.5 × ATR(14)
- TP = SL × RR (range testato: 2:1, 2.5:1, 3:1, 4:1)
- No trade fine anno (evita gap liquidità)

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| BB Period | 10, 14, 20, 30 |
| BB Std Dev | 1.5, 2.0, 2.5 |
| Squeeze soglia | 10°, 15°, 20°, 25°, 30° percentile bandwidth |
| RR | 2:1, 2.5:1, 3:1, 4:1 |
| TF | M1, M5, M15 |
| Simbolo | EURUSD |
| Periodo | 2020-2025 |

## Totale test: 720

## Risultati
### Profittabilità per TF
| TF | Test | Profittevoli | % | Best PF |
|----|------|-------------|---|---------|
| M15 | 240 | 43 | **18%** | 1.22 |
| M5 | 240 | 0 | **0%** | <1.0 |
| M1 | 240 | 9 | **4%** | 1.05 |

### Top 5
| TF | BB p | Std | Squeeze | RR | Trades | WR | PF |
|----|------|-----|---------|-----|--------|-----|-----|
| M15 | 20 | 2.5 | 25° | 4:1 | 840 | 23% | **1.22** |
| M15 | 14 | 2.5 | 30° | 4:1 | 820 | 22% | **1.14** |
| M15 | 20 | 2.5 | 30° | 4:1 | 883 | 22% | **1.11** |
| M15 | 30 | 2.5 | 20° | 3:1 | 678 | 27% | **1.10** |
| M15 | 20 | 2.0 | 25° | 4:1 | 1373 | 22% | **1.10** |

## Pattern emersi
1. **M15 unico TF con edge** (18% profittevole). M5 = zero edge, M1 = edge marginale
2. **BB Period 20 + StdDev 2.5** = migliore combo (cattura cicli volatilità settimanale)
3. **Squeeze al 25° percentile** = sweet spot: né troppo raro né troppo frequente
4. **RR 4:1** domina: WR basso (21-23%) ma vincite compensano
5. **StdDev 2.5 > 2.0 > 1.5**: bande più larghe = breakout più genuini, meno noise

## Confronto con altri concetti
| Metrica | MA Cross | Derivate | RSI | **BB Squeeze** |
|---------|----------|----------|-----|----------------|
| % profittevoli | 3% | 12% | **77%** | 18% |
| Best PF | 1.13 | **2.70** | 1.59 | 1.22 |
| TF ideale | M1 | M5 | M1 | M15 |
| Robustezza | Bassa | Media | **Alta** | Bassa-Media |

## Lezione per il bot finale
> BB Squeeze ha **edge debole come standalone** (PF max 1.22).
> Il vero valore è come **filtro di regime**: quando bandwidth è compressa,
> il mercato è in accumulo/distribuzione. Usare come condizione permissiva
> insieme a FFT (ciclo dominante) per timing del breakout.
> Combinazione suggerita: squeeze BB + segnale FFT breakout stesso verso
> → alta probabilità di espansione direzionale.

## Stato
- [x] Backtest grid search completato (720 test)
- [x] Fogli Excel aggiunti (BB_SUMMARY, BB_ALL, BB_M1/M5/M15)
- [x] Grafici gaussiani inclusi in GAUSSIAN_ANALYSIS
- [x] Scheda strategia in STRATEGY_DESCRIPTIONS
