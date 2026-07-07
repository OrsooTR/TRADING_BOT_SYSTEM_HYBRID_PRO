# 2. Dati, pulizia e lettura del mercato

## Dataset reale usato come riferimento

Nel corpus e' presente una serie minute su EURUSD (`eurusd_m1_2020_2025_combined.csv`). Un estratto iniziale mostra struttura OHLC standard con volume nullo su molte barre forex interbank.

| Campo | Significato |
|---|---|
| datetime | timestamp della barra |
| open | apertura |
| high | massimo |
| low | minimo |
| close | chiusura |
| volume | volume registrato |

## Osservazioni preliminari sul campione analizzato

Su un campione iniziale di 100000 righe:
- media prezzo close circa 1.1016;
- deviazione standard del close circa 0.0157;
- deviazione standard dei rendimenti minuti circa 0.000178;
- skewness positiva;
- curtosi molto alta, quindi code grasse e outlier non trascurabili.

Questa combinazione indica che il mercato non si comporta come una gaussiana semplice e che il modello deve tollerare regime shift, spike e cluster di volatilita'.

## Pulizia minima necessaria

1. Ordinare per tempo.
2. Verificare duplicati.
3. Controllare buchi o barre anomale.
4. Uniformare timezone.
5. Separare training, validation e test.
6. Trattare i rendimenti come oggetto principale, non solo il prezzo.

## Perché il prezzo da solo non basta

Il prezzo e' una traiettoria cumulata. Per il trading quantitativo interessano anche:
- differenze discrete;
- log-return;
- volatilita' realizzata;
- range intrabar;
- continuita' o discontinuita' del regime.

## Chart di riferimento

![EURUSD close e SMA 50](assets/eurusd_close_sma.png)

![Prime e seconde differenze](assets/eurusd_derivatives.png)

## Lettura operativa

Il prezzo grezzo e' utile per visualizzare il contesto, ma il motore deve ragionare su:
- pendenza locale;
- curvatura;
- distanza da media;
- ampiezza del movimento;
- varianza recente;
- posizione rispetto a ciclo e pattern.

## Implicazione per il backtest

Un backtest corretto deve conservare il dato originale e, in parallelo, derivarne una vista feature-based. In pratica:
- OHLC per la simulazione;
- returns per il rischio;
- FFT per il ciclo;
- derivate per il timing;
- pattern per la direzione condizionata.
