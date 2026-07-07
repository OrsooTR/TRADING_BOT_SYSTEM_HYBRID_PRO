# 5. Estrazione del segnale: Wiener-Kolmogorov, Butterworth e processi band-limited

## Nucleo concettuale

Il documento sulle signal extraction methods insiste su un'idea precisa: il segnale osservato e' una somma di componenti che si possono filtrare in modo ottimale se si conosce abbastanza della loro struttura statistica.

La forma classica e':

$$
y(t) = \xi(t) + \eta(t)
$$

dove:
- $\xi(t)$ = segnale;
- $\eta(t)$ = rumore.

## Estimatori di Wiener-Kolmogorov

Per serie finite, gli stimatori minimi in senso quadratico sono:

$$
\hat\xi = \Omega_\xi(\Omega_\xi + \Omega_\eta)^{-1}y
$$

$$
\hat\eta = \Omega_\eta(\Omega_\xi + \Omega_\eta)^{-1}y
$$

Queste formule esprimono l'idea di separare il dato in due parti che si spiegano reciprocamente.

## Filtri Butterworth

Il Butterworth digitale viene usato come prototipo di filtro con transizione regolare:

$$
|H(\omega)|^2 = \frac{1}{1 + (\omega/\omega_c)^{2n}}
$$

Dove:
- $\omega_c$ = frequenza di taglio;
- $n$ = ordine del filtro.

Un ordine maggiore produce una transizione piu' netta ma aumenta il rischio di eccesso di fase e instabilita' pratica.

## Band-limited processes

Il documento evidenzia che alcuni processi sono band-limited: la loro energia vive in bande separate da zone di silenzio spettrale. Per il progetto questo significa:
- non tutte le frequenze sono uguali;
- ci sono zone informative;
- il filtro deve rispettare la separazione tra bande.

## Forme operative nel trading

| Oggetto | Lettura |
|---|---|
| banda bassa | trend macro |
| banda media | swing e cicli intermedi |
| banda alta | microstruttura / rumore |
| dead space | intervallo di scarsa informazione |

## Confronto con Kalman

Il testo di Pollock sottolinea che il Kalman e' potente ma complesso. Nel progetto la lezione e':
- usare il minimo modello sufficiente;
- non complicare se il filtro locale basta;
- preferire una struttura testabile e spiegabile.

## Pipeline consigliata

1. filtro anti-rumore;
2. FFT per stimare la banda;
3. ricostruzione a banda limitata;
4. derivata del segnale filtrato;
5. decisione con regole di contesto;
6. backtest sul risultato.

## Chart di supporto

![Schematico strutturale frattale](assets/fractal_schematic.png)
