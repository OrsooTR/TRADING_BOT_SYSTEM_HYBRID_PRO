---
title: Session Time Cluster
type: strategy_idea
status: da_testare
priority: medium
numero: 09
source: compendium_cap_8_16
---

# 09 — Session Time Cluster

## Ipotesi
Esistono fasce orarie dove la distribuzione dei rendimenti futuri è sistematicamente sbilanciata — non dipende dalla strategia usata ma dalla struttura intraday del mercato (aperture, sovrapposizioni sessioni, fix orari). Testare questo come concetto standalone prima di usarlo come filtro su altri segnali.

## Logica operativa
1. Per ogni ora UTC (0-23) calcolare la distribuzione dei rendimenti sulle prossime N barre
2. Identificare cluster con rendimento medio, win rate, o PF statisticamente diverso dalla media
3. Usare il cluster come gate binario: ora attiva / ora inattiva
4. Testare su tutte le strategie già validate come filtro aggiuntivo

## Feature da calcolare
- `hour_of_day`: ora UTC del segnale (0-23)
- `session_label`: asian / london / newyork / overlap / off
- `hour_avg_return`: rendimento medio delle prossime N barre per quell'ora
- `hour_win_rate`: % barre positive per quell'ora
- `hour_pf`: profit factor empirico per quell'ora su serie storica

## Parametri da testare
| Parametro | Valori |
|-----------|--------|
| Finestra look-forward (N barre) | 1, 3, 5 |
| Metrica di classificazione | win_rate, avg_return, PF |
| Soglia attivazione | top 25%, top 33%, top 50% |
| TF | M1, M5, M15 |

## Backtest minimo
- Train 2020-2023: calcolare distribuzione per ora
- OOS 2024-2025: validare se le ore migliori in-sample restano migliori
- Metriche: PF per fascia oraria, stabilità IS vs OOS

## Rischi noti
- Overfitting: 24 ore = molte combinazioni → usare soglie robuste, non ottimali
- Il pattern orario può cambiare con le stagioni (DST) o cambi di regime macro
- Correlazione con la sessione già testata nell'ATR e Ribbon — non è concetto nuovo se è solo London

## Relazione con altri concetti
- Prerequisito per capire dove i segnali #11, #17 funzionano meglio
- Complementare a [[fft_clock_trigger_hft_filter]] (#14) che guarda i clock via FFT

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
