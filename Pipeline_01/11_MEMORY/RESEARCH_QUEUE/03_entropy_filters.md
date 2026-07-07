# Entropy Filters

## Priorità
P2

## Idea
L'entropia misura quanto un sistema è ordinato o casuale.
Nel trading può essere usata per capire se il mercato sta mostrando struttura o disordine.

## Perché è utile nel progetto
Se il mercato ha bassa entropia locale, potrebbe esserci una struttura più leggibile.
Se l'entropia cresce, il movimento diventa più casuale e i segnali tecnici possono perdere qualità.

## Ipotesi di ricerca
- Entropia bassa = mercato più strutturato.
- Entropia alta = mercato più rumoroso.
- L'entropia può rafforzare il meta-filtro dei regimi.

## Come testarla
1. Calcolare entropia su finestre rolling.
2. Confrontare con regime FFT e risultati backtest.
3. Verificare se filtra bene i periodi di rumore.

## Rischi
- Definizione dell'entropia non banale.
- Sensibilità ai parametri.
- Possibile scarsa robustezza cross-market.

## Criterio di utilità
Valida solo se aiuta a bloccare periodi poco leggibili senza perdere troppo edge.
