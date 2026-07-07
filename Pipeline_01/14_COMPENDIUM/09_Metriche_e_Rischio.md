# 9. Metriche, rischio e validazione

## Metriche di base

| Metricas | Formula sintetica | Uso |
|---|---|---|
| Return | $(V_t - V_{t-1})/V_{t-1}$ | performance semplice |
| Log-return | $\ln(V_t/V_{t-1})$ | additivita' |
| Win rate | trade vincenti / trade totali | frequenza |
| Sharpe | media eccedenza / deviazione standard | efficienza rischio |
| Max drawdown | picco meno valle successiva | peggior perdita |
| Profit factor | gross profit / gross loss | bilancio del sistema |
| Expectancy | $p\cdot win - (1-p)\cdot loss$ | valore atteso |

## Drawdown

Il drawdown e' la metrica che piu' penalizza i sistemi fragili. Un sistema puo' avere buon win rate e fallire comunque per:
- perdite rare ma enormi;
- sequenze di trade avversi;
- leva eccessiva;
- assenza di stop coerenti.

## Validazione corretta

1. In-sample: costruzione.
2. Out-of-sample: verifica su dati non visti.
3. Walk-forward: stabilita' nel tempo.
4. Stress test: slippage, spread, shock, dati mancanti.
5. Regime test: trend, range, volatilita' alta, volatilita' bassa.

## Regola di sopravvivenza

Il motore non deve cercare solo il massimo profitto teorico, ma:
- drawdown accettabile;
- stabilita' temporale;
- assenza di overfitting;
- relazione chiara tra entry e rischio.

## Lettura operativa

Un sistema puo' essere considerato utile solo se i risultati rimangono leggibili su:
- periodi diversi;
- asset diversi;
- timeframe diversi;
- condizioni di mercato differenti.

## Collegamento con il dataset

Il dataset EURUSD minute e' adatto a:
- test di trend;
- test di micro-struttura;
- ricerca di cicli;
- confronto tra filtraggio e rumore.
