# Backtest Derivatives EURUSD ALL_TFS

## Related Notes
- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/04_BACKTEST/DERIVATIVE_tests/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]
- [[../../../Pipeline_01/09_LOGS/report_giornata_2026-04-22]]
- [[derivatives_report_all_tfs_smoke]]
- [[derivatives_report_m15_full]]

- Generated: 2026-04-22 09:58:34 UTC
- Mode: full grid
- Combinations: 1575
- Ranking: OOS Profit Factor desc, OOS Max DD asc, OOS P&L desc

# 02 — Derivatives 1st/2nd Order

## Concetto

- **d1** = derivata prima di EMA(close) = rate of change (velocità/momentum)
- **d2** = derivata seconda di d1 = accelerazione

### Entry Rules

**Threshold mode**: LONG se d1 > threshold E d2 > 0 (momentum positivo E accelerando) **Cross-zero mode**: LONG se d1 cross above 0 E d2 > 0

### Exit: SL = 1.5 × ATR(14), TP = SL × RR

## Parametri Testati

|Parametro|Valori|
|---|---|
|Smooth (EMA)|10, 20, 50|
|D1 Period|3, 5, 10, 15|
|D2 Period|2, 3, 5 (< d1)|
|Entry Mode|threshold, cross_zero|
|D1 Threshold|0.00005, 0.0001, 0.0002|
|RR|1:1, 1.5:1, 2:1, 3:1, 4:1|
|TF|M1, M5, M15|

## Totale Backtest: 1,575

## Risultati Chiave

### Top 5

|TF|Smooth|D1p|D2p|Mode|Thresh|RR|Trades|WR|PF|
|---|---|---|---|---|---|---|---|---|---|
|M5|50|15|5|threshold|0.0002|1:1|37|73%|**2.70**|
|M5|50|15|2|threshold|0.0002|1:1|40|72%|**2.64**|
|M5|50|15|3|threshold|0.0002|1:1|41|71%|**2.42**|
|M5|50|10|2|threshold|0.0002|1.5:1|50|58%|**2.07**|
|M1|20|3|2|threshold|0.0002|3:1|10|40%|2.00|

### Pattern Emersi

1. **M5 è il TF ideale per le derivate** — PF 2.70 con WR 73%
2. **Smooth=50** domina (filtra noise, cattura solo trend macro)
3. **d1_period=10-15** (ciclo lento) + **d2_period=2-5** (accelerazione rapida) = best
4. **Threshold=0.0002** (2 pip/barra) filtra efficacemente il rumore
5. **RR 1:1 domina su M5** perché il WR è altissimo (70%+)
6. **Cross-zero mode quasi sempre inferiore** a threshold mode
7. M15 edge debole (PF max 1.28), M1 troppo pochi trade per essere robusto
8. Derivate catturano il **punto di svolta** del momentum, non il trend puro

### Lezione per il Bot Finale

> Le derivate 1°/2° ordine sono un **potente segnale di momentum**. Funzionano meglio su M5 perché bilanciano granularità e noise. Smooth=50 + d1=15 + threshold=0.0002 è la configurazione "core". Da combinare con filtro direzionale (MA 50/200 dal concetto 01). Con FFT: usare d2 > 0 come conferma che il ciclo FFT sta accelerando.

## Confronto con MA Cross (Concetto 01)

|Metrica|MA Cross (best)|Derivate (best)|
|---|---|---|
|PF|1.13 (M1 50/150 RR4)|**2.70** (M5 sm50 d1=15 RR1)|
|WR|22%|**73%**|
|TF ideale|M1|M5|
|RR ideale|4:1|1:1|
|Approccio|Momentum lento|Momentum + accelerazione|

**Le derivate sono significativamente superiori all'incrocio MA puro.**

## Nota: limitazioni

- M5 testato su 3 anni (2023-2025), non 6 — serve validazione su periodo completo
- M1 testato su 4 mesi — risultati indicativi
- Pochi trade sulle top config (37-50) — serve accumulazione dati