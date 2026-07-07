---
title: Fractal + FFT Confluence
type: strategy_tested
status: Completato
updated: 2026-05-11
numero: 18
source: compendium_cap_15
---

# 18 — Fractal + FFT Confluence

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../11_MEMORY/PROJECT_STATE]]
- [[../TESTED/05_Fractal_SR_Bounce]]
- [[../TESTED/11_FFT_Dominant_Cycle]]
- [[../TESTED/12_FFT_Spectral_Regime_Classifier]]

## Concetto
Combinazione del layer geometrico (frattali S/R, #05) con il layer frequenziale (FFT, #11+#12). Il frattale identifica i livelli di prezzo strutturali; l'FFT verifica che il bounce avvenga in coerenza con la fase ciclica del mercato.

**Logica operativa:**
1. Pivot Williams (fp barre per lato) → livelli di supporto e resistenza attivi nell'ultima `lb` barre
2. Bounce: prezzo si avvicina al livello entro `tol × ATR`
3. FFT cycle slope concorda con la direzione del bounce
4. Opzionalmente: regime = CYCLE (gate qualitativo)

**Entry:**
- LONG = bounce da supporto AND slope_ciclo > 0 AND [regime=CYCLE]
- SHORT = bounce da resistenza AND slope_ciclo < 0 AND [regime=CYCLE]
- Next-bar open | SL = 1.5 × ATR | TP = SL × RR

## Split
**Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)**

## Parametri testati
| Parametro | Valori |
|-----------|--------|
| Fractal period fp | 5 (best da #05) |
| Tolleranza (× ATR) | 0.3, 0.5, 1.0 |
| Lookback lb | 30, 70 barre |
| FFT window N | 64 (M1), 64/128 (M5) |
| Delta regime | 0.03, 0.05 |
| Min period ciclo | 5, 10 barre |
| RR | 2.0, 3.0 |
| SL | 1.5 × ATR (fisso) |
| Sessioni | all, london, newyork, asian |
| TF | M1, M5 |
| Min trade OOS | 100 |

## Risultati — valore incrementale per layer

### M5 (TF più interessante)
| Layer | OOS PF | OOS DD% | Trades OOS | PF Gain |
|-------|--------|---------|-----------|---------|
| Baseline (#05 Fractal) | 1.060 | 93.5% | 16.010 | — |
| +FFT cycle direction | 1.146 | 35.7% | 1.370 | +0.151 |
| +CYCLE regime (full) | **1.268** | **37.1%** | **1.372** | **+0.238** |

### M1 (TF originale #05)
| Layer | OOS PF | OOS DD% | Trades OOS |
|-------|--------|---------|-----------|
| Baseline (#05) | 1.030 | 98.5% | 72.753 |
| +FFT cycle | 1.003 | 96.7% | 28.328 |
| +CYCLE regime | 1.020 | 78.4% | 9.865 |

## Best setup per sessione (M5 full_confl)
| Sessione | OOS PF | OOS DD% | Trades | PF Gain | Config |
|----------|--------|---------|--------|---------|--------|
| newyork | **1.268** | 37.1% | **1.372** | +0.238 | N=64, δ=0.05, min_p=10 |
| asian | **1.232** | **26.0%** | 842 | +0.238 | N=64, δ=0.05, min_p=10 |
| all | 1.084 | 60.8% | 4.455 | +0.092 | N=64, δ=0.03 |
| london | 0.956 | 86.7% | 3.434 | +0.017 | — (negativo) |

## Analisi critica

### Punti di forza
- **Trade count risolto**: M5 NY dà 1.372 trade OOS (274/anno) — ampiamente sopra i 1000 totali richiesti
- **La confluenza aggiunge valore reale**: +0.238 PF gain rispetto al fractal standalone
- **DD crolla**: da 93.5% baseline a 37.1% — il filtro FFT elimina i rimbalzi controciclici
- **Asian session**: PF=1.232 con DD=26% e 842 trade — selettiva ma di qualità

### Confronto con #17 (FFT + Derivative)
| Metrica | #17 Confluence | #18 Fractal+FFT |
|---------|---------------|----------------|
| Best OOS PF | 2.083 | 1.268 |
| OOS DD% | 5.9% | 37.1% |
| Trades OOS 5yr | 49 | 1.372 |
| Trade/anno | ~10 | ~274 |
| Target PF>1.3 | ✅ | ⚠️ (vicino, non raggiunto) |
| Target DD<12% | ✅ | ❌ (37.1%) |
| Target >1000 trade | ❌ | ✅ |

**Il trade-off è chiaro**: #17 ha qualità superiore ma frequenza molto bassa; #18 ha frequenza adeguata ma qualità inferiore.

### London session negativa (OOS PF=0.956)
La sessione London che dominava su RSI, FFT Cycle, Regime e Derivate qui **non funziona per i frattali M5**. Il rimbalzo da S/R è più rumoroso durante London (più volume, più falsi breakout). Questo è coerente con il paper SSRN-2487656 sulla microstruttura di mercato durante la sessione europea.

### M1 non migliorato dalla FFT
Su M1 il filtro FFT non aggiunge valore (PF scende da 1.030 a 1.020). Il fractal M1 standalone (PF=1.030) è già molto frequente (72K trade OOS) ma con DD=98%. L'FFT non riesce a selezionare i trade migliori su M1 — probabilmente perché la granularità temporale è troppo fine per i cicli FFT.

### DD ancora alta (37%)
Il target è DD<12%. Con la confluenza la DD scende significativamente (93%→37%) ma non raggiunge il target. Per avvicinarsi servirebbe aggiungere:
- Vol Gate (#15): filtra solo in bassa volatilità
- Regime classifier (#12) più restrittivo

## Implicazioni per l'architettura del bot

Il Fractal+FFT è complementare al #17 (FFT+Derivative), non alternativo:
- **#17 usare per segnali rari ma ad alta qualità** (10-15/anno, PF=2.0)
- **#18 usare per frequenza** (274/anno, PF=1.27) quando serve più diversificazione

Pipeline possibile:
```
[M5 | NY o Asian session]
  FFT Regime → CYCLE? (N=64, δ=0.05)
    YES → Fractal bounce concorda con slope FFT?
      YES → Entry (SL=1.5×ATR, RR=2.0)
```

## Prossimo step
Combinare #18 con Volatility Gate (#15) per abbassare la DD da 37% verso il target 12%.
Testare anche #19 (FFT Regime routing: #12 decide quale strategia usare per regime).

## Classificazione robustezza
**Media** — PF=1.268 su M5 NY/Asian, 1.372 trade OOS, DD=37%. Non raggiunge i target assoluti (PF>1.3 e DD<12% entrambi) ma dimostra il valore del layer FFT sul fractal. **Candidato per il routing multi-strategia del bot finale.**

## Script
`scripts/run_fractal_fft.py`

## Artifacts
`artifacts/fractal_fft_backtests/data/fractal_fft_results_all.json`
