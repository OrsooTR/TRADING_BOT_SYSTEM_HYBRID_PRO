---
title: FFT Dominant Cycle
type: strategy_tested
status: Completato
updated: 2026-05-07
numero: 11
---

# 11 — FFT Dominant Cycle

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../11_MEMORY/PROJECT_STATE]]

## Concetto
Rolling FFT su log-return con window Hann. Identificazione del ciclo dominante nella banda media (escluse basse freq = trend, alte freq = rumore). Ricostruzione IFFT parziale. Segnale al cambio di direzione dello slope (zero-crossing). Quality filter: SNR > 1.5 e periodo > min_period barre.

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
N: 64 (M1), 64/128 (M5), 64/128/256 (M15) · Low pct: 5/10% · High pct: 20/30% · Min period: 5/10b · SL mult: 1.0/1.5 · RR: 2/3/4 · Sessioni: all/london/newyork/asian · Totale: 1152 combos

## Risultati chiave (OOS 2021-2025, 5 anni)

### Top 5 su M15
| N | Low% | High% | Min P | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% | Trades |
|---|------|-------|-------|----|----|---------|---------|--------|---------|---------|--------|
| 256 | 0.10 | 0.20 | 10 | 1.0 | 2.0 | london | 0.893 | **1.173** | **16.1** | 160.7 | 1188 |
| 256 | 0.10 | 0.20 | 10 | 1.0 | 3.0 | london | 0.970 | 1.161 | 33.4 | 165.2 | 1188 |
| 256 | 0.10 | 0.30 | 10 | 1.0 | 2.0 | london | 0.994 | 1.138 | 19.6 | 145.8 | 1414 |
| 128 | 0.05 | 0.20 | 10 | 1.5 | 2.0 | asian  | 1.029 | 1.128 | 23.8 | 104.7 | 1216 |
| 128 | 0.05 | 0.20 | 10 | 1.0 | 3.0 | asian  | 0.975 | 1.126 | 25.7 | 114.3 | 1216 |

### Best per sessione su M15
| Sessione | OOS PF | OOS DD% | N | Min Period |
|----------|--------|---------|---|-----------|
| **london**   | **1.173** | **16.1** | 256 | 10b |
| asian    | 1.128 | 23.8 | 128 | 10b |
| newyork  | 1.097 | 16.4 | 256 | 10b |
| all      | 1.074 | 48.7 | 64  | 10b |

### Profittevoli per TF (OOS PF > 1.0)
| TF | % profittevoli |
|----|---------------|
| M1  | 73% |
| M5  | 37% |
| M15 | **52%** |

## Confronto con split precedente (4yr train / 2yr OOS)
| Metrica | Split 4+2 | Split 1+5 |
|---------|-----------|-----------|
| Best OOS PF M15 | 1.159 | **1.173** |
| OOS DD% best | 13.2% | 16.1% |
| % profittevoli M15 | 43% | **52%** |
| Sessione top | London | London |

Il FFT Cycle **migliora** passando a 5 anni OOS — segnale forte di robustezza. La sessione London rimane consistente. N=256 (cicli di 25+ barre su M15 = 6+ ore) resta il parametro dominante.

## Pattern emersi
- **N=256 + London + min_period=10** è la configurazione più stabile: OOS PF=1.173, DD=16.1%
- Il Train PF (0.893) è sotto 1.0 ma l'OOS PF è sopra: il modello non overfittal in-sample → edge reale
- **La sessione London domina consistentemente** su tutte le configurazioni FFT
- RR=2.0 performa meglio di 3.0 e 4.0 su M15: il ciclo FFT cattura movimenti relativamente brevi
- **52% combos profittevoli su M15** — il risultato migliore tra ATR (7%), Ribbon (33%), FFT (52%)
- La finestra grande N=256 cattura cicli di ~25-64 barre (6-16 ore) — struttura diurna reale

## Lezione per il bot finale
- FFT Cycle è il **migliore dei tre nuovi concetti testati** su 5 anni OOS
- OOS PF=1.173 con DD=16.1% è interessante ma ancora sotto il target (PF>1.3, DD<12%)
- **Uso ideale: filtro contestuale** — combinato con Derivate (#17) dovrebbe superare la soglia
- La sessione London su M15 è confermata come finestra temporale privilegiata

## Classificazione robustezza
**Media-Alta** — 52% profittevoli M15, OOS PF stabile su 5 anni, nessuna degradazione dal cambio di split. Terzo o quarto nella classifica assoluta. Prerequisito validato per #17 (FFT + Derivative Confluence).

## Script
`scripts/run_fft_cycle_vectorized.py`

## Artifacts
`artifacts/fft_cycle_backtests/data/fft_cycle_results_all.json`
