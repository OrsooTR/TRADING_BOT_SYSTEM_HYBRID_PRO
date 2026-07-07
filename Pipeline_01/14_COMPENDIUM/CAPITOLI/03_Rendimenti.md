---
title: "Rendimenti, log-return e distribuzioni empiriche"
capitolo: 3
tags:
  - rendimenti
  - log-return
  - distribuzione
  - statistica
---

# 3. Rendimenti, log-return e distribuzioni empiriche

> [!info] Navigazione
> [[../INDEX|â† Indice Compendio]] | Capitolo 3 di 26

---

Questo capitolo affronta tradurre il prezzo in variabili che abbiano senso per il rischio e per la misura
dell'edge. L'idea di fondo Ã¨ trattare il mercato come un sistema osservabile, misurabile e correggibile, nel
quale ogni decisione deve essere giustificata da una relazione tra dato, trasformazione e rischio. In questo
quadro il linguaggio tecnico resta centrale, ma viene reso leggibile attraverso una sequenza stabile:
definizione, interpretazione, applicazione e controllo dei limiti. Il risultato atteso non Ã¨ una descrizione astratta
del fenomeno, ma una specifica operativa che possa essere portata dentro il bot.
## 3.1 Nodo operativo
Il prezzo assoluto Ã¨ cumulativo, mentre il rendimento contiene l'informazione utile per la performance. Nel
capitolo dedicato a 3. rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un
vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 3.2 Nodo operativo
Il log-return Ã¨ preferibile quando serve additivitÃ  e comparabilitÃ  su piÃ¹ orizzonti. Nel capitolo dedicato a 3.
rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un vincolo di progetto e
non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando
la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione
non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la
struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma
debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere
testato, comparato e, se necessario, scartato.
## 3.3 Nodo operativo
La distribuzione dei ritorni reali presenta spesso skewness e kurtosis elevate. Nel capitolo dedicato a 3.
rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un vincolo di progetto e
non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando
la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione
non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la
struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma
debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere
testato, comparato e, se necessario, scartato.
## 3.4 Nodo operativo
Le code grasse rendono inadeguata una lettura puramente gaussiana del mercato. Nel capitolo dedicato a 3.
rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un vincolo di progetto e
non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando
la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione
non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la
struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma
debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere
testato, comparato e, se necessario, scartato.
## 3.5 Nodo operativo
La volatilitÃ  deve essere stimata come oggetto dinamico, non come costante del modello. Nel capitolo
dedicato a 3. rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un vincolo di

progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
## 3.6 Nodo operativo
La distribuzione non serve solo a descrivere, ma a dimensionare il rischio e a valutare la fragilitÃ . Nel capitolo
dedicato a 3. rendimenti, log-return e distribuzioni empiriche, questa osservazione va letta come un vincolo di
progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
### Applicazione nel bot
Nel progetto, tradurre il prezzo in variabili che abbiano senso per il rischio e per la misura dell'edge. Il modulo
relativo deve essere misurato con un set di test coerente, altrimenti il vantaggio apparente si dissolve quando
cambiano timeframe, spread o volatilitÃ . Il valore pratico del capitolo sta nel trasformare l'intuizione in una
regola ripetibile, con parametri espliciti e con un criterio chiaro di invalidazione.
### Limiti e errori comuni
Il problema piÃ¹ frequente Ã¨ usare 3. rendimenti, log-return e distribuzioni empiriche come scorciatoia per
prevedere il mercato invece di usarlo come filtro disciplinato. Quando la lettura Ã¨ isolata dal contesto, i segnali
diventano fragili e spesso si degradano in presenza di slippage, shock o regime change. Per questo motivo il
capitolo va letto insieme ai moduli di rischio e validazione, che impediscono di scambiare una buona idea per
un sistema robusto.
Figura 3.1 - Rappresentazione operativa per 3. rendimenti, log-return e distribuzioni empiriche.
Tabella di sintesi operativa
Metrica
Significato
Uso
Mean return
deriva media
contesto
Skewness
asimmetria
bias direzionale
Kurtosis
code grasse
tail risk

VolatilitÃ 
ampiezza
position sizing
### Chiusura del capitolo
Il criterio ultimo Ã¨ semplice: un modulo ha valore solo se aiuta a ridurre rumore, a migliorare timing o a
mantenere la robustezza lungo periodi diversi. Se questo non accade, il modulo resta una ipotesi utile ma non
entra nel nucleo del sistema. 3. Rendimenti, log-return e distribuzioni empiriche viene quindi considerato non
come conclusione, ma come una cella del motore complessivo che va validata, confrontata e, se serve,
sostituita.

---

## Vedi anche
- [[02_Qualita_Dato]]
- [[04_Smoothing]]
- [[20_Metriche]]
