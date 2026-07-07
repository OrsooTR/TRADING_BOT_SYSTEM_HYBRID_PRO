# 03 — RSI Mean-Reversion

## Collegamenti
- [[../INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../04_BACKTEST/INDEX]]
- [[../../05_METRICS/winrate]]
- [[../../05_METRICS/drawdown]]
- [[01_MA_Crossover]]
- [[02_Derivative_1st_2nd_Order]]
- [[04_BB_Squeeze]]

## Concetto
RSI in zona estrema indica possibile esaurimento del movimento corrente e attesa di inversione verso la media.
- **RSI < Oversold** → prezzo ipervenduto → attesa rimbalzo → LONG
- **RSI > Overbought** → prezzo ipercomprato → attesa pullback → SHORT

## Logica operativa
Due modalità di entry:
- **TOUCH**: entra appena RSI scende sotto OS (o sale sopra OB) per la prima volta
- **CROSS**: entra quando RSI torna DENTRO il range (conferma inversione)

## Entry rules
| Direzione | Modalità | Condizione |
|-----------|----------|-----------|
| LONG | Touch | RSI[i] < OS AND RSI[i-1] >= OS |
| LONG | Cross | RSI[i] > OS AND RSI[i-1] <= OS |
| SHORT | Touch | RSI[i] > OB AND RSI[i-1] <= OB |
| SHORT | Cross | RSI[i] < OB AND RSI[i-1] >= OB |

## Risk model
- SL = 1.5 × ATR(14)
- TP = SL × RR (range testato: 1:1, 1.5:1, 2:1, 3:1, 4:1)

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| RSI Period | 7, 9, 14, 21 |
| Overbought | 65, 70, 75, 80 |
| Oversold | 20, 25, 30, 35 |
| Entry Mode | touch, cross |
| RR | 1:1, 1.5:1, 2:1, 3:1, 4:1 |
| TF | M1, M5, M15 |

## Totale test: 1,920

## Risultati
### Profittabilità per TF
| TF | Test | Profittevoli | % | Best PF |
|----|------|-------------|---|---------|
| M1 | 640 | 625 | **98%** | 1.59 |
| M5 | 640 | 531 | **83%** | 1.45 |
| M15 | 640 | 322 | **50%** | 1.20 |

### Top 5
| TF | RSI | OB | OS | Mode | RR | Trades | WR | PF |
|----|-----|-----|-----|------|-----|--------|-----|-----|
| M1 | 21 | 80 | 20 | touch | 1.5 | 66 | 52% | **1.59** |
| M5 | 21 | 80 | 20 | touch | 4.0 | 120 | 27% | **1.45** |
| M1 | 21 | 80 | 20 | touch | 1.0 | 66 | 58% | **1.36** |
| M1 | 21 | 80 | 30 | touch | 2.0 | 527 | 40% | **1.35** |
| M1 | 21 | 80 | 20 | cross | 3.0 | 68 | 31% | **1.34** |

## Pattern emersi
1. **RSI=21 domina su tutti i TF** — periodo lento riduce falsi segnali
2. **OB=80 + OS=20** (estremi) = miglior qualità
3. **Touch mode** migliore su M15, **Cross mode** comparabile su M1
4. RR flessibile: tutti funzionano (WR 55%+ per RR 1:1, WR 25% per RR 4:1)
5. **M15 rsi14 ob65 os35 RR2**: 4211 trade, PF 1.14, P&L +3027% (compounding)

## Lezione per il bot finale
> RSI mean-rev è il concetto PIÙ ROBUSTO (77% test profittevoli).
> RSI=21 come filtro: entra solo quando RSI è estremo.
> Da combinare con FFT: se FFT e RSI concordano sulla direzione → alta conviction.
> OB/OS estremi (80/20) per qualità, larghi (65/35) per quantità di trade.
