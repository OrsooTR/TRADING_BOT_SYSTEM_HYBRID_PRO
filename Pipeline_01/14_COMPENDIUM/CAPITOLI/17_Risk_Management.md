---
title: "Risk management, size, stop loss e take profit"
capitolo: 17
tags:
  - risk-management
  - position-sizing
  - stop-loss
  - take-profit
---

# 17. Risk management, size, stop loss e take profit

> [!info] Navigazione
> [[../INDEX|â† Indice Compendio]] | Capitolo 17 di 26

---

Questo capitolo affronta spostare il focus dal guadagno potenziale alla sopravvivenza del sistema. L'idea di
fondo Ã¨ trattare il mercato come un sistema osservabile, misurabile e correggibile, nel quale ogni decisione
deve essere giustificata da una relazione tra dato, trasformazione e rischio. In questo quadro il linguaggio
tecnico resta centrale, ma viene reso leggibile attraverso una sequenza stabile: definizione, interpretazione,
applicazione e controllo dei limiti. Il risultato atteso non Ã¨ una descrizione astratta del fenomeno, ma una
specifica operativa che possa essere portata dentro il bot.
## 17.1 Nodo operativo
Il rischio va definito prima del profitto, perchÃ© un sistema fragile non accumula vantaggio nel tempo. Nel
capitolo dedicato a 17. risk management, size, stop loss e take profit, questa osservazione va letta come un
vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 17.2 Nodo operativo
La size deve dipendere dalla volatilitÃ , dalla qualitÃ  del segnale e dalla distanza dello stop. Nel capitolo
dedicato a 17. risk management, size, stop loss e take profit, questa osservazione va letta come un vincolo di
progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
## 17.3 Nodo operativo
Il rapporto risk/reward non basta da solo; deve essere valutato insieme alla probabilitÃ  di successo. Nel
capitolo dedicato a 17. risk management, size, stop loss e take profit, questa osservazione va letta come un
vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 17.4 Nodo operativo
Lo stop loss non Ã¨ una punizione, ma il confine che rende l'ipotesi falsificabile. Nel capitolo dedicato a 17. risk
management, size, stop loss e take profit, questa osservazione va letta come un vincolo di progetto e non
come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando la
lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione non
resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la struttura
non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma debole
sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere testato,
comparato e, se necessario, scartato.
## 17.5 Nodo operativo
Il take profit deve essere coerente con la struttura del mercato, non solo con un multiplo arbitrario. Nel
capitolo dedicato a 17. risk management, size, stop loss e take profit, questa osservazione va letta come un

vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 17.6 Nodo operativo
La gestione rischio Ã¨ il cuore della sostenibilitÃ  del bot. Nel capitolo dedicato a 17. risk management, size,
stop loss e take profit, questa osservazione va letta come un vincolo di progetto e non come una nota
accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando la lettura del mercato
con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione non resti statica: ogni
concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la struttura non modifica
almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma debole sul piano
operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere testato, comparato
e, se necessario, scartato.
### Applicazione nel bot
Nel progetto, spostare il focus dal guadagno potenziale alla sopravvivenza del sistema. Il modulo relativo
deve essere misurato con un set di test coerente, altrimenti il vantaggio apparente si dissolve quando
cambiano timeframe, spread o volatilitÃ . Il valore pratico del capitolo sta nel trasformare l'intuizione in una
regola ripetibile, con parametri espliciti e con un criterio chiaro di invalidazione.
### Limiti e errori comuni
Il problema piÃ¹ frequente Ã¨ usare 17. risk management, size, stop loss e take profit come scorciatoia per
prevedere il mercato invece di usarlo come filtro disciplinato. Quando la lettura Ã¨ isolata dal contesto, i segnali
diventano fragili e spesso si degradano in presenza di slippage, shock o regime change. Per questo motivo il
capitolo va letto insieme ai moduli di rischio e validazione, che impediscono di scambiare una buona idea per
un sistema robusto.
Figura 17.1 - Rappresentazione operativa per 17. risk management, size, stop loss e take profit.
Tabella di sintesi operativa
Elemento
Funzione
Errore comune
SL
limite perdita
troppo stretto
TP
obiettivo
troppo distante
Size
esposizione
leva eccessiva

DD
tutela capitale
ignorato
### Chiusura del capitolo
Il criterio ultimo Ã¨ semplice: un modulo ha valore solo se aiuta a ridurre rumore, a migliorare timing o a
mantenere la robustezza lungo periodi diversi. Se questo non accade, il modulo resta una ipotesi utile ma non
entra nel nucleo del sistema. 17. Risk management, size, stop loss e take profit viene quindi considerato non
come conclusione, ma come una cella del motore complessivo che va validata, confrontata e, se serve,
sostituita.

---

## Vedi anche
- [[18_Backtest]]
- [[20_Metriche]]
- [[../../08_EXECUTION/risk_management]]
