# 10. Decision engine e logica del bot

## Obiettivo del decisore

Il decisore non deve essere creativo in senso libero. Deve essere disciplinato, cioe' capace di combinare:
- contesto;
- timing;
- rischio;
- conferma;
- invalidazione.

## Sequenza logica

1. Il mercato e' in trend o in range?
2. Esiste un ciclo dominante?
3. La derivata conferma il verso?
4. Il pattern frattale e' valido?
5. Il rischio e' compatibile con la struttura?
6. L'entry ha un rapporto rischio/rendimento accettabile?
7. Il trade e' ripetibile in backtest?

## Esempio di regola combinata

- se FFT indica banda bassa dominante,
- e la pendenza locale e' positiva,
- e il pattern frattale mostra compressione seguita da breakout,
- allora la strategia puo' passare da osservazione a esecuzione.

## Moduli attualmente presenti nel vault

- MA crossover testato;
- derivata prima e seconda;
- idee FFT trend following;
- confluence frattale-circolare;
- proiezione pattern frattale-FFT;
- risk management;
- broker API;
- dashboard;
- experiment protocol.

## Principio di progetto

Il sistema finale deve rifiutare l'azione quando:
- il segnale e' ambiguo;
- il rumore e' troppo alto;
- il pattern non e' confermato;
- il rischio supera la soglia;
- il regime non e' adatto.

## Logica di memoria

Ogni esperimento deve produrre:
- input;
- ipotesi;
- parametri;
- risultato;
- motivo di successo o fallimento;
- decisione successiva.

Questo e' il meccanismo che trasforma la ricerca in un sistema cumulativo invece che in una sequenza di test isolati.
