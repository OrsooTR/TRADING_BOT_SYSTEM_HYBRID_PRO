---
title: "Merton jump-diffusion e mercato con salti"
capitolo: 23
tags:
  - Merton
  - jump-diffusion
  - salti
  - Poisson
---

# 23. Merton jump-diffusion e mercato con salti

> [!info] Navigazione
> [[../INDEX|â† Indice Compendio]] | Capitolo 23 di 26

---

Questo capitolo affronta spiegare perchÃ© i salti sono fondamentali per la realtÃ  osservabile. L'idea di fondo Ã¨
trattare il mercato come un sistema osservabile, misurabile e correggibile, nel quale ogni decisione deve
essere giustificata da una relazione tra dato, trasformazione e rischio. In questo quadro il linguaggio tecnico
resta centrale, ma viene reso leggibile attraverso una sequenza stabile: definizione, interpretazione,
applicazione e controllo dei limiti. Il risultato atteso non Ã¨ una descrizione astratta del fenomeno, ma una
specifica operativa che possa essere portata dentro il bot.
## 23.1 Nodo operativo
Il modello di Merton introduce eventi discreti che rompono la continuitÃ  del semplice moto browniano. Nel
capitolo dedicato a 23. merton jump-diffusion e mercato con salti, questa osservazione va letta come un
vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura
concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨
che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o
validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul
piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco
che puÃ² essere testato, comparato e, se necessario, scartato.
## 23.2 Nodo operativo
I salti sono coerenti con shock macro, news improvvise e accelerazioni di liquiditÃ . Nel capitolo dedicato a 23.
merton jump-diffusion e mercato con salti, questa osservazione va letta come un vincolo di progetto e non
come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando la
lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione non
resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la struttura
non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma debole
sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere testato,
comparato e, se necessario, scartato.
## 23.3 Nodo operativo
L'aggiunta della componente Poisson rende il modello molto piÃ¹ adatto a un mercato reale. Nel capitolo
dedicato a 23. merton jump-diffusion e mercato con salti, questa osservazione va letta come un vincolo di
progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
## 23.4 Nodo operativo
La presenza di salti cambia la coda della distribuzione e quindi il rischio di perdita estrema. Nel capitolo
dedicato a 23. merton jump-diffusion e mercato con salti, questa osservazione va letta come un vincolo di
progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta,
collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la
descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione.
Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano
teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che
puÃ² essere testato, comparato e, se necessario, scartato.
## 23.5 Nodo operativo
Sul piano operativo questo invita a prevedere gap, slippage e rotture di livello. Nel capitolo dedicato a 23.
merton jump-diffusion e mercato con salti, questa osservazione va letta come un vincolo di progetto e non

come una nota accessoria. Il sistema deve trasformare tale idea in una procedura concreta, collegando la
lettura del mercato con una metrica o con una regola eseguibile. Il punto importante Ã¨ che la descrizione non
resti statica: ogni concetto va associato a un effetto su timing, filtraggio, rischio o validazione. Se la struttura
non modifica almeno uno di questi quattro elementi, allora rimane interessante sul piano teorico ma debole
sul piano operativo. Per questo motivo ogni tema viene interpretato come un blocco che puÃ² essere testato,
comparato e, se necessario, scartato.
## 23.6 Nodo operativo
Il modello jump-diffusion Ã¨ importante perchÃ© mostra come un prezzo possa essere regolare e discontinuo
insieme. Nel capitolo dedicato a 23. merton jump-diffusion e mercato con salti, questa osservazione va letta
come un vincolo di progetto e non come una nota accessoria. Il sistema deve trasformare tale idea in una
procedura concreta, collegando la lettura del mercato con una metrica o con una regola eseguibile. Il punto
importante Ã¨ che la descrizione non resti statica: ogni concetto va associato a un effetto su timing, filtraggio,
rischio o validazione. Se la struttura non modifica almeno uno di questi quattro elementi, allora rimane
interessante sul piano teorico ma debole sul piano operativo. Per questo motivo ogni tema viene interpretato
come un blocco che puÃ² essere testato, comparato e, se necessario, scartato.
### Applicazione nel bot
Nel progetto, spiegare perchÃ© i salti sono fondamentali per la realtÃ  osservabile. Il modulo relativo deve
essere misurato con un set di test coerente, altrimenti il vantaggio apparente si dissolve quando cambiano
timeframe, spread o volatilitÃ . Il valore pratico del capitolo sta nel trasformare l'intuizione in una regola
ripetibile, con parametri espliciti e con un criterio chiaro di invalidazione.
### Limiti e errori comuni
Il problema piÃ¹ frequente Ã¨ usare 23. merton jump-diffusion e mercato con salti come scorciatoia per
prevedere il mercato invece di usarlo come filtro disciplinato. Quando la lettura Ã¨ isolata dal contesto, i segnali
diventano fragili e spesso si degradano in presenza di slippage, shock o regime change. Per questo motivo il
capitolo va letto insieme ai moduli di rischio e validazione, che impediscono di scambiare una buona idea per
un sistema robusto.
Figura 23.1 - Rappresentazione operativa per 23. merton jump-diffusion e mercato con salti.
Tabella di sintesi operativa
Componente
Ruolo
Effetto
Diffusione
rumore continuo
movimento base
Salti
eventi discreti
shock
Rate Poisson
frequenza
intensitÃ 

Jump size
ampiezza
tail risk
### Chiusura del capitolo
Il criterio ultimo Ã¨ semplice: un modulo ha valore solo se aiuta a ridurre rumore, a migliorare timing o a
mantenere la robustezza lungo periodi diversi. Se questo non accade, il modulo resta una ipotesi utile ma non
entra nel nucleo del sistema. 23. Merton jump-diffusion e mercato con salti viene quindi considerato non
come conclusione, ma come una cella del motore complessivo che va validata, confrontata e, se serve,
sostituita.

---

## Vedi anche
- [[22_Black_Scholes]]
- [[24_Variance_Gamma]]
