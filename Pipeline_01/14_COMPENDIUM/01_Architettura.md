# 1. Architettura del sistema ibrido

## Obiettivo generale

Il sistema non nasce come singolo indicatore, ma come catena di trasformazione:

**dati grezzi -> pulizia -> decomposizione -> pattern -> decisione -> esecuzione -> misurazione -> apprendimento**

Il principio di progetto e' conservare solo cio' che produce un vantaggio ripetibile. Il resto rimane ipotesi da testare.

## Strati del motore

| Strato | Funzione | Output |
|---|---|---|
| Data Layer | raccogliere OHLC, volumi, sessioni, spread, eventi | serie pulite e allineate |
| Transform Layer | applicare FFT, derivate, smoothing, filtri | segnali numerici e spettrali |
| Pattern Layer | riconoscere forme frattali, simmetrie, ricorrenze | pattern_id, confidenza, zona |
| Feature Layer | unire ampiezza, fase, pendenza, curvatura, volatilita' | feature vector |
| Decision Engine | combinare regole e filtri | long / short / no trade |
| Risk Layer | size, SL, TP, RR, max exposure | ordine controllato |
| Backtest Layer | misurare edge, robustezza, degrado | report e ranking |
| Logging Layer | memorizzare risultati e anomalie | memoria strutturata |

## Regole di progetto estratte dal vault

- testare un concetto per volta;
- validare prima in isolamento;
- accettare solo combinazioni che migliorano il risultato netto;
- usare risk contenuto;
- impedire che l'ottimizzazione distrugga la generalizzazione;
- non confondere spiegazione teorica e vantaggio operativo.

## Pipeline operativa

1. Normalizzazione dei dati.
2. Estrazione del segnale dominante.
3. Identificazione del contesto di mercato.
4. Verifica di timing con derivate.
5. Confluenza con pattern frattali.
6. Calcolo del rischio e della taglia.
7. Simulazione e logging.
8. Iterazione.

## Criterio di utilita'

Un modulo entra nel sistema finale solo se risponde a tre domande:

- riduce rumore?
- migliora timing o selezione?
- mantiene robustezza su piu' periodi?

Se la risposta e' no, il modulo resta in osservazione.
