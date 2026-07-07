# Wavelet Transform

## Priorità
P1

## Idea
La wavelet transform serve a osservare il mercato su più scale temporali senza perdere completamente il tempo locale.
A differenza della FFT, che tende a descrivere bene i cicli globali ma meno bene i cambi improvvisi, la wavelet permette di vedere dove si concentra l'energia del movimento nel tempo.

## Perché è utile nel progetto
Nel sistema attuale già si ragiona in termini di cicli dominanti e regime. La wavelet può aggiungere una lettura più fine:
- trend lento su scala ampia
- swing intermedi
- micro-movimenti rapidi
- transizioni improvvise di regime

## Ipotesi di ricerca
- I punti di inversione sono più leggibili quando l'energia wavelet cambia di scala.
- La wavelet può migliorare il filtro di qualità sui segnali FFT.
- Le diverse scale possono aiutare a distinguere CYCLE, NOISE e TRANS.

## Come testarla
1. Calcolare coefficienti wavelet su log-return.
2. Separare le scale principali.
3. Confrontare con regime FFT.
4. Misurare miglioramento su entry, drawdown e precisione.

## Rischi
- Aumento della complessità.
- Overfitting sulle scale.
- Costi computazionali maggiori.

## Criterio di utilità
Ha senso solo se riduce i falsi segnali o migliora il timing in modo stabile su più periodi.
