---
title: "Compendio formule matematiche"
tags:
  - formule
  - matematica
  - riferimento
---

# Compendio formule matematiche

> [!info] Navigazione
> [[../INDEX|← Indice Compendio]] | Appendice A1

Raccolta delle 37 appendici formula presenti nel PDF sorgente.
Ogni sezione corrisponde a un blocco formula con descrizione operativa.

---

## Appendice formula 1

Differenze discrete
ΔP_t = P_t - P_{t-1}
Differenze discrete non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La differenza discreta traduce il prezzo in variazione istantanea e serve a valutare la direzione locale. In
pratica questo significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di
invalidazione. Un caso tipico è usare il risultato per selezionare una banda di frequenza, definire la size o
misurare la fragilità della curva equity. Quando la formula non modifica il comportamento del sistema, rimane
un riferimento teorico ma non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata
da un esempio numerico o da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A1 - Lettura visiva collegata a differenze discrete.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 2

Seconda differenza
Δ²P_t = ΔP_t - ΔP_{t-1}
Seconda differenza non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La seconda differenza misura il cambiamento della direzione e funge da proxy per accelerazione o frenata. In
pratica questo significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di
invalidazione. Un caso tipico è usare il risultato per selezionare una banda di frequenza, definire la size o
misurare la fragilità della curva equity. Quando la formula non modifica il comportamento del sistema, rimane
un riferimento teorico ma non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata
da un esempio numerico o da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 3

Return semplice
r_t = (V_t - V_{t-1}) / V_{t-1}
Return semplice non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il rendimento semplice è utile quando si vuole una misura immediata della performance percentuale. In
pratica questo significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di
invalidazione. Un caso tipico è usare il risultato per selezionare una banda di frequenza, definire la size o
misurare la fragilità della curva equity. Quando la formula non modifica il comportamento del sistema, rimane
un riferimento teorico ma non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata
da un esempio numerico o da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A3 - Lettura visiva collegata a return semplice.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 4

Log-return
l_t = ln(V_t / V_{t-1})
Log-return non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
Il log-return è additivo nel tempo e più adatto al confronto tra orizzonti diversi. In pratica questo significa che il
bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare
il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A4 - Lettura visiva collegata a log-return.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 5

Varianza campionaria
s² = Σ(x_i - x■)² / (n - 1)
Varianza campionaria non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la
formula riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre
collocata in un flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge
quando si definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la
stessa equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la
bellezza del simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La varianza sintetizza dispersione e instabilità e, nel trading, è una base per la size. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 6

Deviazione standard
s = √s²
Deviazione standard non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la
formula riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre
collocata in un flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge
quando si definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la
stessa equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la
bellezza del simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La deviazione standard è la radice della varianza e traduce la dispersione nella stessa unità del dato. In
pratica questo significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di
invalidazione. Un caso tipico è usare il risultato per selezionare una banda di frequenza, definire la size o
misurare la fragilità della curva equity. Quando la formula non modifica il comportamento del sistema, rimane
un riferimento teorico ma non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata
da un esempio numerico o da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A6 - Lettura visiva collegata a deviazione standard.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 7

Skewness
γ1 = E[(X-µ)^3] / σ^3
Skewness non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
L'asimmetria segnala se il mercato tende a fare code più pesanti da un lato. In pratica questo significa che il
bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare
il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A7 - Lettura visiva collegata a skewness.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 8

Kurtosis
γ2 = E[(X-µ)^4] / σ^4
Kurtosis non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
La curtosi misura quanto il mercato produce eventi estremi più spesso della gaussiana. In pratica questo
significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso
tipico è usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della
curva equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma
non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o
da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A8 - Lettura visiva collegata a kurtosis.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 9

Trasformata di Fourier continua
X(ω) = ∫ x(t)e^{-iωt} dt
Trasformata di Fourier continua non deve essere letto come un puro esercizio algebrico. Nel sistema di
trading la formula riassume una relazione tra osservazione, trasformazione e decisione, e per questo va
sempre collocata in un flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale
emerge quando si definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia
regime, la stessa equazione può restare formalmente corretta e diventare praticamente poco utile: il punto
non è la bellezza del simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La Fourier continua porta il segnale nel dominio delle frequenze e separa cicli e rumore. In pratica questo
significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso
tipico è usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della
curva equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma
non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o
da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A9 - Lettura visiva collegata a trasformata di fourier continua.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 10

Inversa di Fourier
x(t) = (1/2π)∫ X(ω)e^{iωt} dω
Inversa di Fourier non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
L'inversa ricostruisce il segnale partendo dallo spettro filtrato. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A10 - Lettura visiva collegata a inversa di fourier.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 11

DFT
X_k = Σ x_n e^{-i2πkn/N}
DFT non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume una
relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
La DFT è la versione discreta, indispensabile quando si lavora su finestre finite. In pratica questo significa che
il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A11 - Lettura visiva collegata a dft.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 12

IDFT
x_n = (1/N)Σ X_k e^{i2πkn/N}
IDFT non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume una
relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
L'IDFT consente di ricostruire il segnale dopo aver selezionato solo alcune bande. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A12 - Lettura visiva collegata a idft.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 13

Parseval
Σ|x_n|² = (1/N)Σ|X_k|²
Parseval non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
L'energia del segnale non sparisce, cambia solo dominio di rappresentazione. In pratica questo significa che
il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A13 - Lettura visiva collegata a parseval.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 14

Convoluzione
(f * g)(t) = ∫ f(τ)g(t-τ)dτ
Convoluzione non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La convoluzione descrive il filtraggio e spiega come un kernel modifichi la serie. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A14 - Lettura visiva collegata a convoluzione.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 15

Shift temporale
x(t - t0) ↔ X(ω)e^{-iωt0}
Shift temporale non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Lo spostamento nel tempo produce una rotazione di fase nello spettro. In pratica questo significa che il bot
deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A15 - Lettura visiva collegata a shift temporale.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 16

Modulazione
x(t)e^{iω0 t} ↔ X(ω-ω0)
Modulazione non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La modulazione trasla lo spettro e aiuta a leggere le bande attive. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A16 - Lettura visiva collegata a modulazione.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 17

Sampling theorem
f_s ≥ 2f_max
Sampling theorem non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il campionamento deve essere sufficiente per evitare aliasing. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A17 - Lettura visiva collegata a sampling theorem.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 18

Aliasing
f_alias = |f - kf_s|
Aliasing non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
Quando il sampling è insufficiente una frequenza alta si ripiega su una più bassa. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A18 - Lettura visiva collegata a aliasing.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 19

Butterworth
|H(ω)|² = 1 / [1 + (ω/ω_c)^{2n}]
Butterworth non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il Butterworth offre una transizione regolare tra banda passante e attenuata. In pratica questo significa che il
bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare
il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A19 - Lettura visiva collegata a butterworth.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 20

Wiener-Kolmogorov
■ = Ω_s(Ω_s + Ω_n)^{-1}y
Wiener-Kolmogorov non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Lo stimatore ottimo combina covarianze di segnale e rumore. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A20 - Lettura visiva collegata a wiener-kolmogorov.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 21

Funzione caratteristica
φ_X(u) = E[e^{iuX}]
Funzione caratteristica non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la
formula riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre
collocata in un flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge
quando si definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la
stessa equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la
bellezza del simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La funzione caratteristica codifica distribuzione, cumulanti e pricing via Fourier. In pratica questo significa che
il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 22

Cumulante
κ(u) = ln φ_X(u)
Cumulante non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
I cumulanti permettono di leggere media, varianza, skewness e curtosi in modo compatto. In pratica questo
significa che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso
tipico è usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della
curva equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma
non un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o
da una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A22 - Lettura visiva collegata a cumulante.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 23

Lévy-Khinchine
ψ(u)= iub - ½σ²u² + ∫(e^{iux}-1-iux1_{|x|<1})ν(dx)
Lévy-Khinchine non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La decomposizione Lévy descrive drift, diffusione e salti. In pratica questo significa che il bot deve associare
la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il risultato per
selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity. Quando la
formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un vantaggio
competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una lettura
grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A23 - Lettura visiva collegata a lévy-khinchine.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 24

Brownian motion
dS_t = µS_tdt + σS_t dW_t
Brownian motion non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il moto browniano è il caso base continuo del pricing classico. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A24 - Lettura visiva collegata a brownian motion.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 25

Poisson process
P(N_t=k)=e^{-λt}(λt)^k / k!
Poisson process non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il processo di Poisson conta eventi discreti e modella i salti. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A25 - Lettura visiva collegata a poisson process.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 26

Black-Scholes call
C = S_0N(d1) - Ke^{-rT}N(d2)
Black-Scholes call non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il caso classico resta il benchmark per confrontare modelli più complessi. In pratica questo significa che il bot
deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A26 - Lettura visiva collegata a black-scholes call.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 27

Merton
dS/S = µdt + σdW + (J-1)dN_t
Merton non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
Il modello jump-diffusion introduce shock discreti e code più realistiche. In pratica questo significa che il bot
deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A27 - Lettura visiva collegata a merton.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 28

Variance Gamma
X_t = θG_t + σW_{G_t}
Variance Gamma non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La subordinazione produce asimmetria e code pesanti senza imporre salti separati. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A28 - Lettura visiva collegata a variance gamma.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 29

Drawdown
DD_t = (M_t - E_t) / M_t
Drawdown non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il drawdown misura il massimo dolore subito dal capitale. In pratica questo significa che il bot deve associare
la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il risultato per
selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity. Quando la
formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un vantaggio
competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una lettura
grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A29 - Lettura visiva collegata a drawdown.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 30

Sharpe ratio
Sharpe = (R_p - R_f) / σ_p
Sharpe ratio non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
La Sharpe valuta l'efficienza del rendimento rispetto alla volatilità. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A30 - Lettura visiva collegata a sharpe ratio.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 31

Expectancy
E = p·W - (1-p)·L
Expectancy non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
L'expectancy stima il valore atteso di un trade al netto di win rate e loss medio. In pratica questo significa che
il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A31 - Lettura visiva collegata a expectancy.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 32

Kelly fraction
f* = p - (1-p)/b
Kelly fraction non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Il criterio di Kelly aiuta a evitare sovraesposizione quando il vantaggio è misurabile. In pratica questo significa
che il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A32 - Lettura visiva collegata a kelly fraction.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 33

ATR
ATR = EMA(TR, n)
ATR non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume una
relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
L'ATR è una misura pratica dell'ampiezza del rischio intrabar. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A33 - Lettura visiva collegata a atr.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 34

EMA
EMA_t = αP_t + (1-α)EMA_{t-1}
EMA non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume una
relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
La media esponenziale reagisce più in fretta della media semplice. In pratica questo significa che il bot deve
associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A34 - Lettura visiva collegata a ema.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 35

MACD
MACD = EMA_{12} - EMA_{26}
MACD non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume
una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
Il MACD riassume momentum e divergenza tra medie di diversa velocità. In pratica questo significa che il bot
deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il
risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity.
Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un
vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una
lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A35 - Lettura visiva collegata a macd.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 36

RSI
RSI = 100 - 100/(1+RS)
RSI non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula riassume una
relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un flusso
operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si definisce
cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa equazione
può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del simbolo,
ma la sua capacità di restare stabile quando il contesto muta.
L'RSI misura la forza relativa dei movimenti recenti. In pratica questo significa che il bot deve associare la
formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è usare il risultato per
selezionare una banda di frequenza, definire la size o misurare la fragilità della curva equity. Quando la
formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non un vantaggio
competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da una lettura
grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A36 - Lettura visiva collegata a rsi.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

## Appendice formula 37

Monte Carlo
E^{(i)}_t = E_0 + Σ r^{(i)}_t
Monte Carlo non deve essere letto come un puro esercizio algebrico. Nel sistema di trading la formula
riassume una relazione tra osservazione, trasformazione e decisione, e per questo va sempre collocata in un
flusso operativo. La scrittura compatta serve a evitare ambiguità, ma il significato reale emerge quando si
definisce cosa entra, cosa esce e quale errore si vuole controllare. Se il mercato cambia regime, la stessa
equazione può restare formalmente corretta e diventare praticamente poco utile: il punto non è la bellezza del
simbolo, ma la sua capacità di restare stabile quando il contesto muta.
Le simulazioni Monte Carlo valutano la fragilità dell'equity a sequenze casuali. In pratica questo significa che
il bot deve associare la formula a una metrica, a un filtro o a una regola di invalidazione. Un caso tipico è
usare il risultato per selezionare una banda di frequenza, definire la size o misurare la fragilità della curva
equity. Quando la formula non modifica il comportamento del sistema, rimane un riferimento teorico ma non
un vantaggio competitivo. Per questo ogni formula va sempre accompagnata da un esempio numerico o da
una lettura grafica che ne mostri gli effetti su dati reali o sintetici.
Dal punto di vista della validazione, la domanda non è se la formula sia corretta in astratto, ma se produca
una decisione che migliori l'aspettativa del trade oppure la qualità del filtro. Questo è il criterio con cui si
distinguono gli strumenti utili dai concetti solo descrittivi. Se la trasformazione riduce il rumore, migliora la
localizzazione del ciclo, limita il drawdown o rende più leggibile il rischio, allora può entrare nel motore.
Altrimenti va conservata come riferimento matematico, ma non deve guidare il sistema in automatico.
Figura A37 - Lettura visiva collegata a monte carlo.
Schema di lettura
Voce
Significato
Uso nel trading
Formula
relazione compatta
input del modulo
Interpretazione
cosa misura
lettura del segnale
Limite
dove fallisce
condizione da testare
Osservazione finale: la formula entra nel sistema solo se migliora una scelta concreta. Nel contesto del
trading questo significa che deve ridurre l'incertezza, rendere più pulita la lettura del contesto oppure offrire
un supporto misurabile al backtest.

---

