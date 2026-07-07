---
title: Butterworth Filter as Trend Signal
type: strategy_idea
status: da_testare
priority: high
numero: 13
source: compendium_cap_9
---

# 13 — Butterworth Filter as Trend Signal

## Ipotesi
Un filtro Butterworth passa-basso è teoricamente superiore all'EMA come stimatore della componente strutturale del prezzo: ha risposta piatta nella banda passante (nessuna distorsione delle frequenze lente) e un taglio più netto verso le alte frequenze. Testarlo come segnale direzionale standalone in sostituzione dell'EMA nella strategia EMA Ribbon.

## Logica operativa
1. Applicare filtro Butterworth di ordine K con frequenza di taglio fc al prezzo di chiusura
2. Segnale: prezzo > Butterworth lento → long bias; prezzo < Butterworth lento → short bias
3. Oppure: Butterworth veloce > Butterworth lento → long (analogo al ribbon)
4. Entry: next-bar open · SL = sl_mult × ATR · TP = RR × SL

## Differenza rispetto all'EMA
| Proprietà | EMA | Butterworth |
|-----------|-----|-------------|
| Risposta in banda passante | Decrescente | Piatta (< 3dB) |
| Taglio alle alte freq | Graduale | Più netto |
| Fase | Ritardo variabile | Ritardo uniforme |
| Complessità | Triviale | Scipy (sosfilt) |

## Parametri da gridare
| Parametro | Valori |
|-----------|--------|
| Ordine filtro K | 1, 2, 4 |
| Frequenza di taglio fc | 0.05, 0.10, 0.20 (come frazione di Nyquist) |
| Modalità | singolo filtro vs due filtri (fast/slow) |
| sl_atr_mult | 1.0, 1.5 |
| RR | 2.0, 3.0 |
| Session | all, london, newyork, asian |
| TF | M1, M5, M15 |

## Backtest minimo
- Train 2020-2023, OOS 2024-2025
- Confronto diretto: Butterworth signal vs EMA Ribbon (PF 1.196 M15)
- Stessa logica di entrata (flip del segnale filtrato)

## Rischi noti
- Filtro a fase lineare introduce ritardo fisso → accettabile ma da misurare
- Ordine alto → transiente iniziale lungo (warmup bars)
- `scipy.signal.sosfilt` è causal ma va inizializzato correttamente per evitare artefatti

## Note dal compendium
- Il filtro Butterworth ha risposta monotona: nessun ripple nella banda passante né in quella attenuata
- È il filtro consigliato per separazione in frequenza con parametri interpretabili
- Da usare in coppia con la FFT: FFT per trovare la banda utile, Butterworth per isolarla

## Relazione con altri concetti
- Alternativa diretta all'EMA in [[../TESTED/08_EMA_Ribbon_Direction]] (#08)
- Prerequisito per il filtraggio ottimale nel [[fft_derivative_confluence]] (#17)

## Implementazione Python
```python
from scipy.signal import butter, sosfilt
sos = butter(N=order, Wn=fc, btype='low', output='sos')
filtered = sosfilt(sos, close_array)
```

## Collegamenti
- [[../INDEX]]
- [[../../04_BACKTEST/INDEX]]
- [[../../11_MEMORY/DEVELOPMENT_BACKLOG]]
