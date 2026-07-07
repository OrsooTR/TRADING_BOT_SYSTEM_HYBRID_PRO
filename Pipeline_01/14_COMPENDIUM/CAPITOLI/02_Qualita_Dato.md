---
title: "QualitÃ  del dato, preprocessing e integritÃ  del campione"
capitolo: 2
tags:
  - dati
  - preprocessing
  - OHLCV
---

# 2. QualitÃ  del dato, preprocessing e integritÃ  del campione

> [!info] Navigazione
> [[../INDEX|â† Indice Compendio]] | Capitolo 2 di 26

---

Questo capitolo affronta spiegare perchÃ© il dataset va trattato come materiale statistico e non come semplice
grafico. L'idea di fondo Ã¨ trattare il mercato come un sistema osservabile, misurabile e correggibile, nel quale
ogni decisione deve essere giustificata da una relazione tra dato, trasformazione e rischio. In questo quadro il
linguaggio tecnico resta centrale, ma viene reso leggibile attraverso una sequenza stabile: definizione,
interpretazione, applicazione e controllo dei limiti. Il risultato atteso non Ã¨ una descrizione astratta del
fenomeno, ma una specifica operativa che possa essere portata dentro il bot.
## 2.1 Nodo operativo
Il timestamp Ã¨ la prima variabile critica, perchÃ© un errore di allineamento altera rendimenti, cicli e volatilitÃ .
Nel capitolo dedicato a 2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va
letta come un vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in
una procedura concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il
punto importante Ã¨ che la descrizione non resti statica: ogni concetto va associato a un effetto su timing,
filtraggio, rischio o validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora
rimane interessante sul piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene
interpretato come un blocco che puÃ² essere testato, comparato e, se necessario, scartato.
## 2.2 Nodo operativo
Duplicati, buchi e barre anomale devono essere gestiti prima di qualunque backtest. Nel capitolo dedicato a
2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va letta come un vincolo di
progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
## 2.3 Nodo operativo
Nel forex, il volume puÃ² essere incompleto: il motore deve usare anche range e volatilitÃ  intrabar. Nel capitolo
dedicato a 2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va letta come un
vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 2.4 Nodo operativo
L'osservazione del prezzo deve essere accompagnata da una vista su log-return e differenze discrete. Nel
capitolo dedicato a 2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va letta
come un vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una
procedura concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto
importante Ã¨ che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio,
rischio o validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane
interessante sul piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato
come un blocco che puÃ² essere testato, comparato e, se necessario, scartato.
## 2.5 Nodo operativo
La suddivisione training, validation e test Ã¨ necessaria per evitare che il filtro impari solo il passato. Nel
capitolo dedicato a 2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va letta

come un vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una
procedura concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto
importante Ã¨ che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio,
rischio o validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane
interessante sul piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato
come un blocco che puÃ² essere testato, comparato e, se necessario, scartato.
## 2.6 Nodo operativo
Ogni anomalia deve essere classificata come evento di mercato, errore dati o effetto microstrutturale. Nel
capitolo dedicato a 2. qualitÃ  del dato, preprocessing e integritÃ  del campione, questa osservazione va letta
come un vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una
procedura concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto
importante Ã¨ che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio,
rischio o validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane
interessante sul piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato
come un blocco che puÃ² essere testato, comparato e, se necessario, scartato.
### Applicazione nel bot
Nel progetto, spiegare perchÃ© il dataset va trattato come materiale statistico e non come semplice grafico. Il
modulo relativo deve essere misurato con un set di test coerente, altrimenti il vantaggio apparente si dissolve
quando cambiano timeframe, spread o volatilitÃ . Il valore pratico del capitolo sta nel trasformare l'intuizione in
una regola ripetibile, con parametri espliciti e con un criterio chiaro di invalidazione.
### Limiti e errori comuni
Il problema piÃ¹ frequente Ã¨ usare 2. qualitÃ  del dato, preprocessing e integritÃ  del campione come scorciatoia
per prevedere il mercato invece di usarlo come filtro disciplinato. Quando la lettura Ã¨ isolata dal contesto, i
segnali diventano fragili e spesso si degradano in presenza di slippage, shock o regime change. Per questo
motivo il capitolo va letto insieme ai moduli di rischio e validazione, che impediscono di scambiare una buona
idea per un sistema robusto.
Figura 2.1 - Rappresentazione operativa per 2. qualitÃ  del dato, preprocessing e integritÃ  del campione.
Tabella di sintesi operativa
Controllo
Rischio se assente
Azione
Duplicati
bias sui ritorni
deduplica
Gap
falsi segnali
riempimento o esclusione
Timezone
slittamento regime
normalizzazione

Outlier
varianza distorta
flag e robustezza
### Chiusura del capitolo
Il criterio ultimo Ã¨ semplice: un modulo ha valore solo se aiuta a ridurre rumore, a migliorare timing o a
mantenere la robustezza lungo periodi diversi. Se questo non accade, il modulo resta una ipotesi utile ma non
entra nel nucleo del sistema. 2. QualitÃ  del dato, preprocessing e integritÃ  del campione viene quindi
considerato non come conclusione, ma come una cella del motore complessivo che va validata, confrontata
e, se serve, sostituita.

---

## Vedi anche
- [[01_Architettura]]
- [[03_Rendimenti]]
- [[../../02_DATA/data_pipeline]]
