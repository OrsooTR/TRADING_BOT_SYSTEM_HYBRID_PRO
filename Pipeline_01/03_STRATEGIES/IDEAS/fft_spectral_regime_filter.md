---
title: FFT Spectral Regime Classifier
type: strategy_idea
status: da_testare
priority: high
numero: 12
source: compendium_cap_11_16 ssrn-2487656
---

# 12 — FFT Spectral Regime Classifier

## Ipotesi
La distribuzione dell'energia spettrale sui log-return distingue regimi di mercato: energia concentrata sulle basse frequenze → trend; energia distribuita uniformemente → rumore/range; picco in banda media → ciclo di swing. Non genera entry ma abilita o disabilita le strategie esistenti.

## Bande operative (da compendium cap. 11)
| Banda | Interpretazione | Uso |
|-------|----------------|-----|
| Bassa (bin 1-10%) | Trend profondo | Filtro lento, bias direzionale |
| Media (bin 10-40%) | Ciclo / swing | Setup e timing |
| Alta (bin 40-100%) | Rumore microstrutturale | Eliminare, anti-falsi segnali |
| Dead space | Separazione netta | Zona di taglio ideale |

## Feature da calcolare
- `low_freq_power`: potenza normalizzata in banda bassa
- `mid_freq_power`: potenza normalizzata in banda media
- `high_freq_power`: potenza normalizzata in banda alta
- `hf_ratio = high_freq_power / total_power`
- `spectral_slope`: pendenza log-log dei bin (random walk puro ≈ -1)
- `dominant_period`: bin dominante (eredita da #11)
- `regime_label`: trend / cycle / noise / transition

## Regole di classificazione
- `low_freq_power > 0.50` → regime = trend
- `mid_freq_power > 0.40` → regime = cycle
- `hf_ratio > 0.55` → regime = noise
- nessuna dominanza → regime = transition (no trade)

## Parametri da gridare
| Parametro | Valori |
|-----------|--------|
| Finestra FFT N | 64, 128, 256 |
| Soglia trend | 0.40, 0.50 |
| Soglia ciclo | 0.35, 0.45 |
| Soglia rumore | 0.50, 0.60 |
| TF | M1, M5, M15 |

## Backtest minimo
- Test A: misurare rendimento medio delle prossime N barre per regime (classificazione pura)
- Test B: applicare come filtro alle Derivate (#02, PF 2.70) — il PF aumenta?
- Test C: applicare come filtro a RSI (#03, PF 1.59) nel regime "cycle"
- Train 2020-2023, OOS 2024-2025

## Metriche chiave
- Rendimento medio per label di regime (stabile in OOS?)
- Distribuzione del regime nel tempo (quante barre sono "trend" vs "noise"?)
- Delta PF rispetto alle strategie base con e senza filtro

## Rischi noti
- Classificazione sensibile alla lunghezza della finestra FFT
- Regime "transition" può essere troppo frequente → riduce i trade utili
- La potenza spettrale è influenzata dal trend di finestra → detrending necessario prima

## Note dal compendium (cap. 11)
- Non tutte le frequenze hanno la stessa dignità informativa
- I dead spaces spettrali permettono un filtraggio più netto e meno ambiguo
- Il filtro deve rispettare la banda utile senza forzare ricostruzione artificiale

## Prerequisiti
- [ ] #11 FFT Dominant Cycle testato (fornisce `dominant_period` e `band_ratio`)

## Relazione con altri concetti
- Versione FFT del [[volatility_regime_gate]] (#15) che usa invece ATR percentile
- Alimenta il routing nel [[fft_derivative_confluence]] (#17)
- Fondamento del layer regime nell'architettura finale del bot

## Regole da paper accademici (SSRN 2487656)
- Costruire baseline spettrale prima del segnale
- Non interpretare picchi calendario come edge direzionali senza controllo
- Usare picchi ad alta frequenza come filtro di microstruttura

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../01_THEORY/FFT/ssrn_2487656_intraday_patterns_ng_futures]]
- [[fft_dominant_cycle]]
- [[../TESTED/02_Derivative_1st_2nd_Order]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
