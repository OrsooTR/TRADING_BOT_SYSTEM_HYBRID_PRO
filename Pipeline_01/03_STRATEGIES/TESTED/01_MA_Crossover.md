# 01 - MA Crossover

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../05_METRICS/INDEX]]
- [[../../08_EXECUTION/risk_management]]
- [[../../09_LOGS/report_giornata_2026-04-22]]

## Concetto
Due medie mobili:
- Fast > Slow -> long
- Fast < Slow -> short
- SL = 1.5 x ATR(14)
- TP = SL x RR

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| Fast MA | 5, 10, 15, 20, 30, 50 |
| Slow MA | 20, 50, 100, 150, 200 |
| RR | 1:1, 1.5:1, 2:1, 3:1, 4:1 |
| TF | M1, M5, M15 |
| Simbolo | EURUSD |
| Periodo | 2020-2025 |

## Risultati chiave
### Top 5
| TF | Fast | Slow | RR | PF | DD | P&L% |
|----|------|------|----|----|----|------|
| M1 | 50 | 150 | 4 | 1.13 | 55 | 1018.6 |
| M1 | 50 | 150 | 3 | 1.12 | 48.5 | 728.4 |
| M1 | 50 | 200 | 4 | 1.08 | 46.0 | 1120.3 |
| M1 | 50 | 150 | 2 | 1.06 | 69.7 | 169.6 |
| M1 | 50 | 200 | 3 | 1.05 | 44.1 | 477.3 |

## Pattern emersi
- M1 e il timeframe migliore
- M5 ha edge molto debole
- M15 ha edge limitato
- Fast 50 e Slow 150-200 sono i filtri piu robusti
- RR 3 e 4 sono il driver del risultato
- DD troppo alto per una strategia standalone

## Lezione per il bot finale
Le MA lente hanno valore soprattutto come regime filter, non come entry signal definitiva.

## Riferimenti
- workbook MA crossover esterno
- [[../../02_DATA/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
