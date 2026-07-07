# Regole di Progettazione - Bot Ibrido PRO

## Collegamenti
- [[Vision]]
- [[Roadmap]]
- [[../03_STRATEGIES/INDEX]]
- [[../04_BACKTEST/INDEX]]
- [[../08_EXECUTION/risk_management]]
- [[../11_MEMORY/DECISIONS_LOG]]
- [[../13_PDF_LIBRARY/academic_sources]]

## Filosofia
Testare un concetto alla volta in isolamento, poi combinare solo quelli con edge validato.

## Split standard
`Train: 2020 (1 anno) | OOS: 2021-2025 (5 anni)` - applicato a tutti i backtest, decisione definitiva confermata il 2026-05-08.

## Pipeline di test
`Concetto singolo -> grid search -> validazione OOS -> candidato`

## Concetti da testare

### Layer 1 - Segnali base (standalone)
- [x] 01 - [[../03_STRATEGIES/TESTED/01_MA_Crossover|MA Crossover]] - PF 1.13 M1, regime filter, non entry
- [x] 02 - [[../03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order|Derivate 1 e 2 Ordine]] - PF 2.70 M5, momentum puro
- [x] 03 - [[../03_STRATEGIES/TESTED/03_RSI_MeanReversion|RSI Mean-Reversion]] - PF 1.59 M1, 77% profittevoli
- [x] 04 - [[../03_STRATEGIES/TESTED/04_BB_Squeeze|Bollinger Band Squeeze + Breakout]] - PF 1.22 M15, debole
- [x] 05 - [[../03_STRATEGIES/TESTED/07_ATR_Channel_Breakout|ATR Channel Breakout]] - PF 1.09 M15, 7% profittevoli OOS 5yr, debole
- [x] 06 - [[../03_STRATEGIES/TESTED/06_VWAP_TrendTrading|VWAP Trend Trading]] - PF 1.16 M1, sessione LonNY
- [x] 07 - [[../03_STRATEGIES/TESTED/05_Fractal_SR_Bounce|Fractal S/R Bounce]] - PF 1.18 M1, 68% profittevoli
- [x] 08 - [[../03_STRATEGIES/TESTED/08_EMA_Ribbon_Direction|EMA Ribbon Direction Filter]] - PF 1.10 M15, 33% profittevoli OOS 5yr, asian
- [ ] 09 - [[../03_STRATEGIES/IDEAS/session_time_cluster|Session Time Cluster]] - fasce orarie con edge sistematico
- [ ] 10 - Candle pattern - solo se oggettivizzabile con regole precise

### Layer 2 - FFT (nucleo del sistema)
- [x] 11 - [[../03_STRATEGIES/TESTED/11_FFT_Dominant_Cycle|FFT Dominant Cycle]] - PF 1.173 M15, 52% profittevoli OOS 5yr, London N=256
- [x] 12 - [[12_FFT_Spectral_Regime_Classifier|FFT Spectral Regime Classifier]] - banda dominante + energia relativa -> label regime
- [ ] 13 - [[../03_STRATEGIES/IDEAS/butterworth_trend_filter|Butterworth Filter as Trend Signal]] - filtro passa-basso vs EMA, confronto tecnico
- [x] 14 - [[../03_STRATEGIES/TESTED/14_FFT_Clock_Trigger_HFT_Filter|FFT Clock Trigger HFT Filter]] — RSI +0.065 NY +0.023 London · terzo layer filtro meccanico

### Layer 3 - Meta-filtri e regime
- [x] 15 - [[../03_STRATEGIES/TESTED/15_Volatility_Regime_Gate|Volatility Regime Gate]] - valido soprattutto su RSI low-vol, molto piu debole su Derivate high-vol
- [ ] 16 - [[../03_STRATEGIES/IDEAS/jump_spike_filter|Jump / Spike Filter]] - esclusione barre Merton-style dalle code

### Layer 4 - Confluenza (combinazioni)
- [x] 17 - [[../03_STRATEGIES/TESTED/17_FFT_Derivative_Confluence|FFT + Derivative Confluence]] - OOS PF=1.707 DD=7.8% M15 London · PRIMA STRATEGIA TARGET RAGGIUNTO
- [x] 18 - [[../03_STRATEGIES/TESTED/18_Fractal_FFT_Confluence|Fractal + FFT Confluence]] - PF 1.268 DD 37% M5 NY/Asian · 1372 trade 5yr · frequenza OK
- [ ] 19 - [[../03_STRATEGIES/IDEAS/fft_spectral_regime_filter|FFT Regime + Strategy Routing]] - #12 attiva #03/#02/#06 per regime

### Layer 5 - Ricerca avanzata
- [ ] 20 - [[../03_STRATEGIES/IDEAS/seasonal_ecm_exogenous_signal|Seasonal ECM Exogenous Signal]] - cointegration per regime
- [ ] 21 - [[../03_STRATEGIES/IDEAS/momentum_volume_lifecycle|Momentum Volume Lifecycle]] - fasi accumulo/distribuzione
- [ ] 22 - [[../03_STRATEGIES/IDEAS/fft_trend_following|FFT Trend Following]] - segnale FFT puro senza derivate

## Regole fisse
1. Max RR = 1:4
2. SL basato su ATR
3. Risk per trade contenuto
4. No trade fine anno
5. Backtest su almeno 3 anni
6. Split train/test obbligatorio
7. Ogni segnale FFT deve essere confrontato con una baseline strutturale di calendario/sessione
8. Un picco FFT e valido solo se e stabile su finestre rolling e confermato OOS
9. Separare frequenze direzionali da frequenze di microstruttura/HFT
10. Ogni strategia momentum deve includere almeno un filtro volume o regime
11. Le variabili esogene vanno testate per regime/stagione prima del campione aggregato

## Checklist tecnica FFT

Questa checklist vale per tutti i concetti dal #11 in poi.

- [ ] Definire una baseline strutturale di sessione/calendario prima di interpretare un picco FFT come edge
- [ ] Usare log-return o serie detrended quando la trasformazione richiede stazionarieta locale
- [ ] Applicare windowing esplicito e controllare aliasing / leakage
- [ ] Distinguere almeno quattro zone: trend, ciclo utile, rumore, microstruttura
- [ ] Convertire il picco spettrale in periodo leggibile e verificare che abbia senso sul timeframe
- [ ] Verificare persistenza rolling del picco o della banda utile in train e OOS
- [ ] Introdurre no-trade logic quando i segnali non convergono o il regime e ambiguo
- [ ] Eseguire sensitivity check sui parametri chiave (N, bande, soglie, filtri)
- [ ] Eseguire almeno una forma di walk-forward o stabilita per finestra prima della promozione
- [ ] Trattare i filtri FFT come contesto/regime salvo prova forte del contrario

## Metriche di accettazione
| Metrica | Soglia minima |
|---------|---------------|
| PF | > 1.3 |
| DD | < 12% |
| Trade/anno | > 50 |
| WR | > 25% se RR alto |
| OOS degradation | < 40% |
| Peak persistence FFT | stabile in train e OOS |
| Regime stability | edge presente in almeno 2 finestre walk-forward |

## Architettura bot finale
`Regime Filter (FFT) -> Entry Signal (Derivate/Frattali) -> Conviction Score -> Execution`

## Regole importate dai paper accademici

### SSRN 2487656
- Prima del segnale: costruire baseline spettrale della struttura di mercato
- Non interpretare picchi giornalieri, settimanali o intraminuto come edge direzionali senza controllo
- Usare picchi ad alta frequenza come possibile filtro di rumore/microstruttura
- Testare NUFFT/FFT e, se i dati sono irregolari, un controllo Lomb-Scargle o equivalente
- Per variabili esogene, usare split di regime: stagione, sessione, macro regime o volatilita

### SSRN 1734526
- Momentum e reversal vanno letti come ciclo informativo, non solo come rendimento passato
- Volume alto dopo momentum maturo puo segnalare ingresso tardivo e rischio reversal
- Distinguere low volume winner, high volume winner, high volume loser e low volume loser
- Il cambio di giudizio degli operatori si osserva come cambio di holding e quindi come volume

### Compendium tecnico (2026-05-07)
- FFT non prevede il prezzo: separa bande informative (trend/ciclo/rumore)
- Il segnale migliore e una convergenza tra FFT (contesto) + derivate (timing) + frattali (geometria)
- I dead spaces spettrali tra bande sono preziosi per il filtraggio netto
- Il mercato non va ridotto a una sola forma di rumore: compatibilita con distribuzioni non gaussiane
- La no-trade logic e parte della performance, non un fallimento del sistema
- Walk-forward, sensitivity e controllo overfitting sono gate di promozione, non optional
- Butterworth va usato come riferimento operativo di filtraggio, non come dogma
