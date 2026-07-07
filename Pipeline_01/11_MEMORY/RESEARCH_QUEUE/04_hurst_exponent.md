# Hurst Exponent

## Priorità
P1

## Idea
L'Hurst exponent serve a capire se un processo tende a persistere, a essere casuale o a mean-revertire.
Nel trading è utile perché aiuta a distinguere mercati con comportamento diverso.

## Perché è utile nel progetto
Può diventare una variabile di regime aggiuntiva:
- H > 0.5 = persistenza
- H ≈ 0.5 = casualità
- H < 0.5 = tendenza al ritorno verso la media

## Ipotesi di ricerca
- In regime persistente, la strategy momentum dovrebbe funzionare meglio.
- In regime mean-reverting, le strategie di rientro verso la media dovrebbero essere superiori.
- L'Hurst può aiutare a scegliere il tipo di entry.

## Come testarla
1. Calcolare Hurst su finestra rolling.
2. Segmentare i risultati dei backtest per livelli di H.
3. Valutare se i risultati cambiano davvero.

## Rischi
- Stima rumorosa sulle finestre corte.
- Interpretazione eccessiva di differenze piccole.

## Criterio di utilità
Serve solo se aggiunge una separazione reale tra regimi operativi.
