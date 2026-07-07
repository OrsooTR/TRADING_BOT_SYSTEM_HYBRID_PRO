# Volatility Clustering

## Priorità
P1

## Idea
La volatilità tende a raggrupparsi: periodi tranquilli sono spesso seguiti da altri periodi tranquilli, e periodi turbolenti da altri turbolenti.
Questo è un fatto molto utile perché il mercato non cambia umore in modo casuale ogni barra.

## Perché è utile nel progetto
Il sistema può usare il clustering della volatilità per:
- capire quando il rumore sta aumentando
- anticipare fasi di espansione
- modificare la soglia di ingresso
- adattare il rischio

## Ipotesi di ricerca
- Le strategie che funzionano in bassa volatilità falliscono in alta volatilità.
- Il clustering può migliorare i filtri di regime.

## Come testarla
1. Calcolare volatilità rolling.
2. Osservare i cluster.
3. Relazionarli ai risultati di trading.

## Criterio di utilità
Utile se aiuta a proteggere il sistema dai momenti di destabilizzazione.
