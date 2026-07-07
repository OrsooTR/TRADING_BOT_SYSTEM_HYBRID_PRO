# Strategia Idea - Fractal Circular Confluence

## Collegamenti
- [[../INDEX]]
- [[../../01_THEORY/FRACTALS/fractal_circular_indicator]]
- [[../../01_THEORY/FRACTALS/pattern_library]]
- [[../../01_THEORY/FFT/applicazione_trading]]
- [[../../01_THEORY/DERIVATES/derivata_prima]]
- [[../../06_AGENT_LOGIC/decision_system]]

## Idea
Usare il Fractal Circular Indicator non come segnale diretto, ma come layer di confluenza geometrico-temporale.

## Tesi operativa
Il mercato reagisce con maggiore probabilita quando prezzo e tempo convergono in una zona con:
- nodo ciclico vicino
- geometria circolare favorevole
- intersezione con diagonale
- prossimita a livello armonico
- conferma dinamica di `d1` e `d2`

## Input richiesti
- pivot principali
- nodi temporali del ciclo
- cerchi o ellissi normalizzati
- diagonali strutturali
- livelli Fibonacci
- `FFT signal`
- `d1`
- `d2`

## Feature candidate
- `cycle_phase`
- `time_to_next_node`
- `distance_to_nearest_circle`
- `distance_to_diagonal`
- `distance_to_center_axis`
- `fib_confluence_score`
- `geometric_confluence_score`
- `fft_cycle_score`
- `d1`
- `d2`

## Esempio di logica long
- area vicina a nodo ciclico
- prezzo in o vicino a reaction zone geometrica
- `fib_confluence_score` sopra soglia
- `d1 > 0`
- `d2 > 0`
- ciclo FFT non contrario

## Esempio di logica short
- area vicina a nodo ciclico
- prezzo in o vicino a reaction zone geometrica
- `fib_confluence_score` sopra soglia
- `d1 < 0`
- `d2 < 0`
- ciclo FFT non contrario

## Uscite possibili
- target su zona geometrica successiva
- uscita su nodo temporale successivo
- uscita per invalidazione della simmetria
- stop basato su ATR e perdita della confluenza

## Rischi
- scelta discrezionale dei pivot
- geometria instabile se non normalizzata
- overfitting visivo
- scarsa trasferibilita se il modello dipende dal chart rendering

## Primo esperimento minimo
- un solo asset
- un solo timeframe
- ancoraggio pivot automatico
- una sola famiglia geometrica
- test IS/OOS con event study su turning windows

## Obiettivo
Capire se la confluenza geometrica aggiunge edge misurabile sopra la coppia `FFT + d1 + d2`.
