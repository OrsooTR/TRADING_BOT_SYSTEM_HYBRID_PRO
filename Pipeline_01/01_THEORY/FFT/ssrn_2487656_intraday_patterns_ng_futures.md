---
title: "SSRN 2487656 - Intraday Patterns in Natural Gas Futures"
type: academic_source
topic:
  - fft
  - nufft
  - lomb_scargle
  - hft
  - cointegration
status: integrated
source_pdf: "../../assets/pdfs/academic/ssrn-2487656.pdf"
---

# SSRN 2487656 - Intraday Patterns in Natural Gas Futures

## Identita fonte

Paper: *Intraday Patterns in Natural Gas Futures: Extracting Signals from High-Frequency Trading Data*.

Autori: Jung Heon Song, Marcos Lopez de Prado, Horst D. Simon, Kesheng Wu.

Tema: uso di strumenti di signal processing per leggere pattern intraday, componenti spettrali e segnali di trading algoritmico nei futures sul natural gas.

## Idea centrale

Il paper mostra che l'analisi in frequenza puo separare pattern strutturali del mercato da pattern generati dall'attivita di trading. La parte piu utile per il bot e la distinzione tra:

- frequenze attese per struttura del mercato;
- frequenze persistenti nei prezzi;
- picchi anomali ad alta frequenza;
- attivita concentrata nei primi secondi del minuto;
- relazione stagionale tra variabile esogena e prezzo tramite cointegration.

## Punti teorici rilevanti

### 1. Baseline strutturale del mercato

Prima di interpretare lo spettro dei prezzi, il paper costruisce una funzione binaria di mercato aperto/chiuso. Lo spettro di questa funzione diventa la baseline strutturale.

Implicazione per il vault: non basta trovare un picco FFT. Bisogna chiedersi se quel picco deriva dal calendario del mercato, dalla sessione, da aperture/chiusure o da reale comportamento di prezzo.

### 2. Frequenze operative

Il paper usa frequenze espresse in cicli per anno:

- 1 = ciclo annuale;
- 52 = ciclo settimanale;
- 365/366 = ciclo giornaliero;
- 8760 = ciclo orario;
- 525600/527040 = ciclo al minuto.

Implicazione: nel nostro bot conviene convertire ogni frequenza FFT in periodo leggibile, per esempio minuti, ore, sessioni o giorni.

### 3. Picchi persistenti

Nei dati NG futures 2007-2013 i picchi piu stabili sono giornalieri, bisettimanali/settimanali e armoniche collegate alla struttura operativa. La persistenza multi-anno e piu importante del singolo picco isolato.

Regola: un picco FFT diventa feature solo se e stabile su finestre multiple e non sparisce fuori campione.

### 4. Alta frequenza e HFT

Il paper confronta la forza dei picchi ad alta frequenza con la baseline strutturale. Quando la pendenza power-law e meno negativa della baseline, le alte frequenze sono relativamente piu forti del previsto.

Implicazione: una crescita della potenza ad alta frequenza puo essere interpretata come regime di microstruttura rumorosa/HFT, non necessariamente come segnale direzionale.

### 5. Picco una volta al minuto

Il paper trova un picco persistente intorno a una volta al minuto. La precisione del picco suggerisce attivita sistematica, probabilmente ordini basati su clock come TWAP/VWAP.

Implicazione: per EURUSD o XAUUSD M1/M5 non bisogna ignorare il calendario interno della candela. Anche senza dati tick, la chiusura di ogni minuto puo incorporare flussi meccanici.

### 6. Primo secondo del minuto

Sui dati filtrati, molti massimi di volume ricadono nei primi secondi del minuto. Questo indica clock-triggered trading.

Implicazione: se in futuro avremo dati tick o second-level, una feature chiave sara la quota di volume nei primi secondi della candela.

### 7. Lomb-Scargle come controllo

Il paper confronta NUFFT e Lomb-Scargle per dati non uniformi. Lomb-Scargle gestisce meglio certe irregolarita temporali, ma nel caso studiato NUFFT cattura meglio alcune frequenze coerenti con meccanismi di mercato noti.

Regola: usare un secondo metodo spettrale come controllo quando i dati sono non uniformi o hanno gap.

### 8. Cointegration stagionale con variabili esogene

La cointegration tra temperatura prevista e prezzo del natural gas fallisce sul campione intero, ma funziona quando il campione viene diviso per stagioni. Il driver esogeno cambia segno o forza a seconda del regime stagionale.

Implicazione: una variabile esogena non va testata su tutto il campione senza regime split. Il test va fatto per stagione, sessione o regime.

## Concetti backtestabili generati

- [[../../03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]
- [[../../03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]
- [[../../03_STRATEGIES/IDEAS/seasonal_ecm_exogenous_signal]]

## Regole operative da importare

- Costruire sempre una baseline strutturale prima di usare picchi FFT come edge.
- Accettare un picco FFT solo se persistente in train e OOS.
- Separare frequenze direzionali da frequenze di microstruttura.
- Testare la robustezza su finestre rolling.
- Quando una variabile esogena e plausibile, testarla per regime/stagione prima del campione aggregato.

## Collegamenti

- [[teoria_base]]
- [[applicazione_trading]]
- [[../../04_BACKTEST/INDEX]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../13_PDF_LIBRARY/academic_sources]]
