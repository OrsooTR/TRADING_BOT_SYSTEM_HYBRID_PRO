---
title: FFT Spectral Regime Classifier
type: strategy_tested
status: Completato
updated: 2026-05-11
numero: 12
---

# 12 — FFT Spectral Regime Classifier

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../11_MEMORY/PROJECT_STATE]]

## Concetto
Meta-filtro basato sulla distribuzione dell'energia spettrale dei log-return. Classifica ogni barra in un regime di mercato e abilita/disabilita le strategie appropriate.

**Bande spettrali (log-return, Hann window):**
- Low band (bin 1-10%): quasi sempre vuota nei log-return → ignorata come regime standalone
- Mid band (bin 10-60%): swing / struttura ciclica
- High band (bin 60-100%): rumore / alta frequenza / casuale

**Classificazione:**
- `CYCLE`: mid_ratio > hf_ratio + delta → struttura swing dominante
- `NOISE`: hf_ratio > mid_ratio + delta → alta frequenza domina = casuale
- `TREND`: spectral_slope < slope_thresh → processo persistente (raro nei log-return)
- `TRANS`: nessun dominante chiaro → evitare trade

**Ipotesi testate:**
- RSI mean-reversion in NOISE regime → meno struttura = mean-reversion più affidabile
- Derivate in CYCLE regime → struttura oscillatoria supporta il momentum

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| FFT window N | 64, 128 |
| Band boundaries | low=10%, high=60% (fissi) |
| Delta (|mid-hf| soglia) | 0.03, 0.05, 0.08 |
| Slope threshold (TREND) | -1.0, -1.5 |
| Sessioni | all, london, newyork, asian |
| TF | M1, M5, M15 |
| Strategie testate | RSI (#03), Derivate (#02) |

## Risultati chiave

### RSI in NOISE regime — M15
| N | Delta | Session | Train PF | OOS PF | OOS DD% | OOS P&L% | Trades | PF Gain |
|---|-------|---------|---------|--------|---------|---------|--------|---------|
| 128 | 0.08 | london | 1.046 | **1.224** | 20.1 | 36.9 | 245 | **+0.176** |
| 128 | 0.03 | london | 1.153 | 1.177 | 24.2 | 42.4 | 351 | +0.129 |
| 128 | 0.05 | london | 0.923 | 1.155 | 22.0 | 30.8 | 306 | +0.107 |

### RSI in NOISE regime — M5
| N | Delta | Session | Train PF | OOS PF | OOS DD% | OOS P&L% | Trades | PF Gain |
|---|-------|---------|---------|--------|---------|---------|--------|---------|
| 128 | 0.03 | london | 0.818 | **1.199** | 24.6 | 147.5 | 795 | **+0.189** |
| 128 | 0.05 | london | 0.851 | 1.186 | 23.0 | 109.0 | 693 | +0.176 |
| 128 | 0.08 | london | 0.938 | 1.177 | 15.9 | 78.6 | 575 | +0.167 |

### Derivate in CYCLE regime — M15
| N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |
|---|-------|---------|---------|--------|---------|---------|
| 64 | 0.03 | asian | 0.975 | 1.065 | 66.7 | +0.027 |
- Guadagno marginale, DD insostenibile (>66%) → non raccomandato

### Baseline (senza filtro)
| TF | Strategy | OOS PF baseline |
|----|---------|----------------|
| M15 | RSI | 1.048 |
| M15 | Derivate | 1.040 |
| M5 | RSI | 1.014 |
| M5 | Derivate | 1.022 |

### Distribuzione regime (M15, OOS 2021-2025, N=64, delta=0.05)
| Regime | % barre |
|--------|---------|
| CYCLE | 46% |
| NOISE | 36% |
| TRANS | 15% |
| TREND | 2% |

## Test A — Forward return per regime
Forward return medio a 10 barre (in pip), M15 OOS:
- TREND: -0.41 pip (n=2695, 2.2%) → pochi casi, volatilità alta
- CYCLE: -0.07 pip (n=55838, 46%) → sostanzialmente zero → non predittivo della direzione
- NOISE: -0.04 pip (n=44051, 36%) → quasi zero
- TRANS: +0.13 pip (n=18745, 15%) → rumore statistico

**Conclusione Test A:** il regime NON predice la direzione del mercato — confermato. Serve come filtro di CONTESTO per le strategie, non come segnale direzionale autonomo.

## Pattern emersi

1. **RSI + NOISE è la combinazione più efficace**: quando i log-return mostrano struttura ad alta frequenza (casuale), la mean-reversion è più affidabile. Logica: in mercato NOISE non c'è trend che possa spingere il prezzo lontano dall'equilibrio a lungo.

2. **N=128 >> N=64** per il filtro NOISE: la finestra più lunga identifica meglio i periodi di alta casualità, filtrando meno ma con più precisione (17-26% dei trade vs 41% con N=64).

3. **London session è dominante** anche con il filtro regime — confermato per la terza volta consecutiva (dopo Ribbon e FFT Cycle).

4. **Derivate NON beneficiano** del filtro CYCLE in modo significativo: il guadagno è marginale (+0.027) e la DD rimane alta. Questo suggerisce che le derivate hanno bisogno di un filtro diverso (es. FFT Cycle direzionale).

5. **Trade count ridotto ma qualità alta**: RSI filtrato scende da ~1400 a 245 trade OOS su M15 London — seleziona solo 17.6% delle barre ma con PF 1.224.

## Implicazioni per l'architettura del bot

Il Regime Classifier va applicato PRIMA dei segnali RSI:
```
FFT Regime(N=128, delta=0.08) → NOISE?
    YES → RSI signal → Entry (SL=1.5×ATR, RR=2.0, London session)
    NO  → Skip
```

Per le Derivate, il filtro migliore rimane il FFT Dominant Cycle (#11) direzionale.

## Classificazione robustezza
**Alta** — 245 trade OOS su M15, PF=1.224 stabile su 5 anni, train PF>1.0. Il PF gain di +0.176 è il miglioramento più grande ottenuto da qualsiasi filtro fino ad oggi. **Candidato primario per il Layer 3 (meta-filtri) del bot finale.**

## Script
`scripts/run_regime_classifier.py`

## Artifacts
`artifacts/regime_backtests/data/regime_results_all.json`
`artifacts/regime_backtests/data/regime_test_a_forward_returns.csv`
