# Hilbert Transform

## Priorità
P1

## Idea
La Hilbert transform può essere usata per estrarre fase istantanea, ampiezza istantanea e frequenza istantanea di un segnale.
Nel contesto trading, questo è interessante perché il mercato può essere letto non solo come movimento, ma come oscillazione con una certa fase.

## Perché è utile nel progetto
Il progetto già usa l'idea di ciclo dominante. La Hilbert può aggiungere:
- fase del ciclo
- momento in cui il ciclo sta cambiando
- misura dell'allineamento tra prezzo e ritmo interno

## Ipotesi di ricerca
- Il crossing di fase può anticipare il cambio di direzione.
- La fase istantanea può essere un filtro ulteriore per i segnali FFT.
- L'ampiezza istantanea può aiutare a capire se il ciclo è ancora forte o sta morendo.

## Come testarla
1. Applicare Hilbert al segnale filtrato.
2. Estrarre fase e ampiezza.
3. Cercare relazioni con zero-crossing della derivata.
4. Misurare se le entrate diventano più precise.

## Rischi
- Letture troppo sensibili al rumore.
- Fase instabile su mercati sporchi.
- Difficoltà interpretativa.

## Criterio di utilità
Utile solo se offre una conferma aggiuntiva al ciclo dominante senza introdurre troppo lag.
