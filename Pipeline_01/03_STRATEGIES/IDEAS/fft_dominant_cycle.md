---
title: FFT Dominant Cycle
type: strategy_idea
status: da_testare
priority: high
numero: 11
source: compendium_cap_6_7_11
---

# 11 — FFT Dominant Cycle

## Ipotesi
Il ciclo dominante del mercato — identificato tramite FFT su una finestra rolling di log-return — contiene informazione direzionale: se il ciclo è in fase ascendente il bias è long, se discendente è short. La frequenza dominante va ricalcolata a ogni barra.

## Logica operativa
1. Su finestra rolling N di log-return, applicare window function (Hann) e calcolare FFT
2. Escludere banda bassa (trend di finestra) e banda alta (rumore): isolare banda media
3. Identificare il bin con massima energia → `dominant_period` = N / k_max
4. Ricostruire il segnale con IFFT parziale usando solo quel bin
5. Long se segnale ricostruito crescente (d/dt > 0), Short se decrescente
6. Entry: next-bar open · SL = sl_mult × ATR(14) · TP = RR × SL

## Feature
- `dominant_period`: periodo in barre del ciclo dominante
- `dominant_power_ratio`: energia bin dominante / energia totale
- `cycle_phase`: segnale ricostruito normalizzato [-1, 1]
- `cycle_slope`: derivata discreta del segnale ricostruito
- `band_ratio`: energia banda media / energia totale

## Parametri da gridare
| Parametro | Valori |
|-----------|--------|
| Finestra FFT N | 64, 128, 256 |
| Cutoff banda bassa | 5%, 10% dei bin |
| Cutoff banda alta | 20%, 30% dei bin |
| sl_atr_mult | 1.0, 1.5 |
| RR | 2.0, 3.0 |
| Session | all, london, newyork, asian |
| TF | M1, M5, M15 |

## Backtest minimo
- Train 2020-2023, OOS 2024-2025
- Confronto baseline: EMA Ribbon (PF 1.196 M15)
- Analisi: `dominant_period` stabile nel tempo? Threshold su `dominant_power_ratio`?

## Rischi noti
- Leakage senza windowing → applicare Hann obbligatoriamente
- Ciclo dominante può cambiare improvvisamente (non stazionarietà)
- Lag nella ricostruzione del segnale via IFFT parziale
- Con N piccolo: bassa risoluzione in frequenza

## Note dal compendium
- FFT va applicata sui log-return, non sul prezzo (non stazionario)
- Aliasing e leakage producono segnali falsamente convincenti
- Controllare Nyquist: con barra M15, cicli < 30 min sono invisibili o distorto

## Relazione con altri concetti
- Prerequisito per [[fft_derivative_confluence]] (#17)
- Alimenta [[fft_spectral_regime_filter]] (#12) con `dominant_period`

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../01_THEORY/FFT/teoria_base]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
