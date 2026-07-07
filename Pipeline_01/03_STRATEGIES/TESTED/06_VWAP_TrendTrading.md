# 06 — VWAP Trend Trading

## Collegamenti
- [[../INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../04_BACKTEST/INDEX]]
- [[../../05_METRICS/INDEX]]
- [[../../09_LOGS/report_giornata_2026-04-28]]
- [[../../14_COMPENDIUM/04_FFT_e_Spettro]]
- [[01_MA_Crossover]]
- [[02_Derivative_1st_2nd_Order]]
- [[03_RSI_MeanReversion]]
- [[04_BB_Squeeze]]
- [[05_Fractal_SR_Bounce]]

## Fonte
> Zarattini C., Aziz A. (2023) *"Volume Weighted Average Price (VWAP) — The Holy Grail for Day Trading Systems"*, SSRN 4631351

## Concetto
VWAP di sessione come indicatore di squilibrio di mercato (market imbalance).
- **Prezzo > VWAP** → buyers dominano la sessione → **LONG**
- **Prezzo < VWAP** → sellers dominano la sessione → **SHORT**
- Quando il prezzo "torna" dall'altro lato → squilibrio invertito → **exit e reverse**

### Perché funziona (paper)
Gli investitori istituzionali usano il VWAP come benchmark di esecuzione (~50% degli ordini istituzionali). Questo crea una profezia auto-avverante: quando il prezzo è sopra VWAP, le istituzioni tendono a comprare ancora → il trend si auto-alimenta.

## Formula VWAP
$$VWAP = \frac{\sum HLC3_t \times Vol_t}{\sum Vol_t}$$

**Adattamento EURUSD** (no volume reale):
$$VWAP_{EUR} = \frac{\sum_{t=1}^{n} HLC3_t}{n} = \overline{HLC3}_{sessione}$$
Ogni barra pesa ugualmente (equal-weight). Reset ogni giorno a mezzanotte UTC.

## Entry Rules (fedeli al paper)
| Direzione | Condizione |
|-----------|-----------|
| LONG | close_t > VWAP_t (candela chiude sopra VWAP) |
| SHORT | close_t < VWAP_t (candela chiude sotto VWAP) |
| Exit/Reverse | Candela chiude dall'ALTRO lato del VWAP |
| Fine sessione | Chiude tutte le posizioni aperte |

**IMPORTANTE**: Il paper specifica che si esce SOLO se la candela **chiude** oltre il VWAP — non se il prezzo lo tocca intracandle. Questo riduce i false exit.

## Due Modalità Testate
| Mode | Logica | Caratteristiche |
|------|--------|----------------|
| **Pure** | Exit = candela chiude altro lato VWAP | Fedele al paper, pochi trade di qualità |
| **Fixed** | Entry = VWAP cross, exit = ATR SL + RR fisso | Più trade, risk standardizzato |

## Risk Model
- **Paper originale**: 100% equity per trade (no leverage)
- **Nostra versione**: 0.5% rischio fisso per trade (più conservativo)
- SL tested: 0.5, 0.8, 1.0, 1.5, 2.0 × ATR(14)
- RR tested: 1.5:1, 2:1, 2.5:1, 3:1, 4:1

## Parametri Testati
| Parametro | Valori |
|-----------|--------|
| TF | M1, M5, M15 |
| VWAP Anchor | Giornaliero (reset alle 00:00 UTC) |
| Sessione | 24h, London (7-12), LonNY (7-17), NY (13-20), LonNYeve (7-20) |
| Mode | pure, fixed |
| SL Mult | 0.5, 0.8, 1.0, 1.5, 2.0 |
| RR | 1.5, 2.0, 2.5, 3.0, 4.0 |

## Totale test: 390

## Risultati
### Profittabilità per TF
| TF | Test | Profitable | % | Best PF |
|----|------|-----------|---|---------|
| M1 | 130 | 89 | **68%** | **1.16** |
| M5 | 130 | 57 | **44%** | **1.10** |
| M15 | 130 | 20 | **15%** | **1.05** |

### Top 5
| TF | Session | Mode | SL | RR | Trades | WR | PF |
|----|---------|------|-----|-----|--------|-----|-----|
| M1 | LonNY | pure | auto | auto | 1828 | 12% | **1.16** |
| M1 | LonNY | fixed | 0.5 | 4:1 | 24426 | 22% | **1.14** |
| M1 | NY | fixed | 0.5 | 4:1 | 14485 | 22% | **1.13** |
| M1 | 24h | fixed | 0.5 | 4:1 | 56977 | 22% | **1.13** |
| M1 | London | fixed | 0.5 | 4:1 | 12943 | 22% | **1.12** |

## Pattern Emersi
1. **M1 domina** (68% profittevoli) — granularità ottimale per leggere VWAP cross
2. **Sessione LonNY (7-17 UTC) è il sweet spot** — massima liquidità EURUSD
3. **Pure mode** cattura i trend lunghi con poche operazioni di alta qualità (WR 12%, hit ratio coerente con 17% del paper)
4. **SL piccolo (0.5 ATR) + RR alto (4:1)** = miglior combo per fixed mode
5. **M15 edge quasi nullo** — VWAP cross poco frequenti, segnale troppo ritardato
6. **24h peggio di sessione filtrata** — le ore di bassa liquidità aumentano il noise

## Confronto paper vs EURUSD
| Metrica | Paper (QQQ) | EURUSD M1 (nostro) |
|---------|-------------|-------------------|
| Hit Ratio | 17% | 12-22% |
| Best PF | N/A (retun-based) | 1.16 |
| Ritorno totale | +671% | +1342% (M1 fixed) |
| Edge principale | Trend-following | Trend-following |
| TF ideale | M1 | M1 |
| Filtro sessione | RTH only (9:30-16) | LonNY (7-17 UTC) |

## Lezione per il Bot Finale
> VWAP ha edge reale su EURUSD nonostante la mancanza di volume reale.
> La sessione è il parametro più critico: filtrare su London+NY riduce il noise.
> Uso ideale nel bot: VWAP come **filtro direzionale di bias giornaliero**.
> Se VWAP giornaliero è sopra → preferire long su altri segnali (RSI, FFT).
> Combinare: VWAP bias + RSI mean-rev + Fractal S/R = entry ad alta conviction.

## Stato
- [x] Backtest grid search completato (390 test)
- [x] Fogli Excel aggiunti (VWAP_SUMMARY, VWAP_ALL, VWAP_M1/M5/M15)
- [x] Grafici gaussiani aggiunti in GAUSSIAN_ANALYSIS
- [x] Scheda strategia aggiunta in STRATEGY_DESCRIPTIONS
- [x] Vault Obsidian aggiornato
