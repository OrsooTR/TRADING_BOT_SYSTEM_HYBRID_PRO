# Fractal Circular Indicator

## Collegamenti
- [[INDEX]]
- [[teoria_base]]
- [[pattern_library]]
- [[pythagoras_document_analysis]]
- [[../../03_STRATEGIES/IDEAS/fractal_circular_confluence]]
- [[../../06_AGENT_LOGIC/decision_system]]

## Descrizione sintetica
Il Corrado Malanga Fractal Circular Indicator e un framework visivo di analisi che prova a descrivere il mercato come geometria tempo-prezzo.

Non lavora solo su direzione e livelli.
Prova a combinare:
- pivot frattali
- nodi temporali ciclici
- geometria circolare o ellittica
- diagonali di simmetria o proiezione
- livelli armonici e Fibonacci

## Cosa rappresenta davvero
I 5 livelli logici principali sono:

1. pivot frattali
I massimi e minimi rilevanti vengono usati come ancore iniziali del modello.

2. proiezione temporale ciclica
Le linee verticali future rappresentano possibili turning windows o cambi ciclo.

3. geometria circolare o ellittica
Cerchi e archi descrivono zone di espansione, compressione e ritorno verso equilibrio.

4. simmetria e riflessione
Il futuro viene costruito come trasformazione del passato: riflessione, traslazione, dilatazione, compressione.

5. livelli armonici
I livelli Fibonacci vengono usati come filtri di confluenza e non come trigger isolati.

## Lettura funzionale degli elementi grafici
### Punti blu sulla linea orizzontale
Interpretazione possibile:
- nodi temporali del ciclo
- divisioni di fase
- finestre di accelerazione o decelerazione

Traduzione quant:
- `cycle_phase`
- `time_to_next_node`
- `bars_from_last_node`

### Cerchi o ellissi bianche
Non sono supporti o resistenze classiche.
Rappresentano aree in cui la probabilita di reazione del prezzo puo aumentare.

Traduzione quant:
- `distance_to_nearest_circle`
- `inside_reaction_ellipse`
- `ellipse_pressure_score`

### Diagonali blu
Possono essere lette come:
- traiettorie candidate
- assi di simmetria
- linee di inversione o continuita

Traduzione quant:
- `distance_to_diagonal`
- `diagonal_intersection_count`
- `slope_alignment_score`

### Livelli Fibonacci
Ruolo nel modello:
- filtro armonico
- misura della profondita della correzione
- conferma di confluenza

Traduzione quant:
- `fib_level_bucket`
- `fib_distance_score`
- `fib_confluence_score`

## Ipotesi implicite del modello
- il mercato non e puro rumore
- il tempo conta quanto il prezzo
- gli impulsi e le correzioni hanno una simmetria parziale
- i pattern si deformano ma mantengono identita
- le zone di confluenza hanno piu valore delle barre isolate

## Lettura del setup mostrato su XAUUSD 1H
La struttura visiva suggerisce:
- impulso forte iniziale
- recupero marcato
- correzione
- ritorno in area centrale della geometria

Questa lettura non implica un segnale secco.
Implica piuttosto:
- transizione
- compressione interna
- preparazione del prossimo swing

Messaggio operativo:
la prossima reazione su una zona di confluenza conta piu della singola candela.

## Forza concettuale
La forza dell'indicatore non e il cerchio in se.
La forza e la fusione di:
- tempo
- prezzo
- simmetria
- fasi del ciclo
- geometria di reazione
- proporzioni armoniche

Per questo e piu vicino a un motore di contesto che a un indicatore classico di entrata.

## Limiti principali
### Discrezionalita
Se i pivot vengono scelti a mano, due operatori possono costruire scenari diversi.

### Bias di conferma
Una geometria ricca aumenta il rischio di vedere pattern anche dove non esistono.

### Overfitting geometrico
Piu strutture si aggiungono, piu il passato puo apparire coerente senza che il futuro lo sia davvero.

### Dipendenza dall'ancoraggio
Se il pivot iniziale e scelto male, tutta la geometria successiva si degrada.

### Sensibilita allo scaling del chart
La geometria non deve dipendere dalla resa grafica del grafico ma da coordinate normalizzate.

## Traduzione utile per il bot
Questo indicatore non va usato come oracolo.
Va trasformato in un `Geometry Layer` misurabile.

Feature candidate:
- `anchor_confidence`
- `cycle_phase`
- `time_to_next_node`
- `distance_to_center_axis`
- `distance_to_nearest_circle`
- `distance_to_diagonal`
- `fib_confluence_score`
- `geometric_confluence_score`
- `reaction_zone_flag`
- `swing_symmetry_score`

## Regola operativa suggerita
Non entrare perche il prezzo tocca un cerchio.

Entrare solo se convergono:
- nodo temporale
- zona geometrica
- livello armonico
- conferma di `d1`
- conferma di `d2`
- conferma del ciclo dominante via FFT

## Relazione con il framework del progetto
Questo indicatore non e in concorrenza con la FFT.
Nel progetto puo diventare il layer geometrico sopra la struttura ciclica.

Pipeline proposta:
`FFT -> Derivate -> Fractal Circular Geometry -> Decision Engine`

## Validazione consigliata
1. event study sui nodi temporali
2. event study sulle ellissi
3. test di confluenza tra geometria, Fibonacci e derivate
4. walk-forward OOS con pivot detection automatica

## Sintesi finale
Definizione utile:
`non entry indicator, ma context engine geometrico-temporale`

Frase chiave:
non cerca solo di dire dove va il prezzo, ma in quale punto della geometria tempo-prezzo il mercato e piu incline a reagire.
