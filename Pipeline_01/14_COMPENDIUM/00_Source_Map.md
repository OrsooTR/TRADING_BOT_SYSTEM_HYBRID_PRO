# Mappa delle fonti e dei concetti estratti

Questo nodo raccoglie la traccia di provenienza dei materiali analizzati e la loro traduzione operativa nel vault.

| Fonte | Nucleo concettuale | Uso nel progetto |
|---|---|---|
| ECONSIGS.pdf | Wiener-Kolmogorov, filtri finiti, Butterworth digitale, processi band-limited | Filtri di estrazione segnale e lettura della struttura di frequenza |
| FIVESTAT.pdf | Fourier statistico, DFT, matrice circolante, aliasing, sampling, Parseval | Base teorica per FFT su dati finanziari e controllo della ricostruzione |
| Matsuda Intro FT Pricing.pdf | Fourier transform pricing, characteristic functions, DFT, Black-Scholes, Merton, VG | Ponte tra FFT e pricing di opzioni / modelli di salto |
| fractals.pdf | Libreria di pattern frattali LONG, sequenze da 3 a 6 candele | Pattern matching e catalogo operativo per ingressi e conferme |
| Pythagoras_Trading_Prediction_.pdf | Frattali, proiezione temporale, narrazione coscienza/mercato, Fourier, derivate | Traduzione delle idee frattali in ipotesi testabili e filtri di mercato |

## Regola di lettura
La parte teorica viene separata in tre livelli:

1. **Descrizione matematica**: formule, trasformate, densità, filtri, derivate.
2. **Operativita' di mercato**: entry, timing, conferme, uscita, rischio.
3. **Validazione**: backtest, out-of-sample, metriche, robustezza.

## Nota metodologica
Le componenti filosofiche o speculative presenti in alcuni materiali vengono mantenute come contesto storico o narrativo, ma nel progetto vengono convertite solo nelle parti osservabili e testabili:
- ricorrenza di forme
- trasformazioni invarianti
- cicli dominanti
- accelerazione/decelerazione del prezzo
- metriche verificabili
