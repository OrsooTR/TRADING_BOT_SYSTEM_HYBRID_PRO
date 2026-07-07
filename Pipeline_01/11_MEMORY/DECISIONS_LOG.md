---
title: Decisions Log
type: project_memory
priority: high
updated: 2026-05-08
---

# Decisions Log

## Collegamenti
- [[INDEX]]
- [[PROJECT_STATE]]
- [[DEVELOPMENT_BACKLOG]]
- [[../00_CORE/00_Regole_Progettazione]]
- [[../08_EXECUTION/broker_api]]

## Decisioni confermate
- Il sistema va costruito per layer: dati, trasformazioni, feature, decisione, backtest, logging
- Ogni concetto va testato in isolamento prima di entrare nel bot finale
- Il filtro direzionale MA 50/150-200 e un buon candidato come regime filter
- Stop loss basato su ATR, non fisso in pip
- Il risk per trade desiderato e nell'ordine di meno dell'1% del capitale
- Ogni test importante deve produrre un file markdown dedicato
- I risultati non vanno sovrascritti
- Il materiale Pythagoras entra nel vault come fonte di ricerca, non come prova scientifica
- Il termine "consapevolezza" va tradotto in variabili misurabili e non lasciato come parametro nascosto
- Tra Transform Layer e Decision Engine va considerato un Pattern Layer frattale
- Il Fractal Circular Indicator va trattato come geometry layer di contesto, non come trigger automatico standalone
- Lo split standard definitivo e `Train: 2020 | OOS: 2021-2025` per tutti i backtest
- Il layer FFT va trattato prima come filtro di contesto/regime e solo dopo come candidato di entry standalone
- Ogni concetto FFT deve includere baseline strutturale, no-trade logic e controllo di stabilita parametrica
- Il primo ibrido da privilegiare dopo i filtri di regime e `#17 FFT + Derivative Confluence`

## Insight gia emersi
- Le MA lente sembrano piu utili come filtro che come segnale di ingresso puro
- RR 3:1 e 4:1 sembrano piu sensati del RR basso nei test MA
- M1 ha mostrato piu edge del M5 e M15 nel test MA documentato
- Il PDF Pythagoras e piu utile come blueprint di prodotto che come modello matematico gia validato
- La parte piu promettente del documento e la coppia pattern library + projection engine
- Il valore reale dell'indicatore circolare sta nella confluenza tempo-prezzo, non nel singolo cerchio o livello Fibonacci

## Incoerenze da risolvere
- Target dichiarato: XAU/USD M15
- Test validato finora: EURUSD con edge migliore su M1

- Gate della pipeline: candidato se PF > 1.0
- Metriche minime dichiarate: PF > 1.3 e DD < 12%

- Risk management generico: rischio per trade < 1-2%
- Regola fissa altrove: 0.3-1.0% del capitale

- Split vecchio presente in alcuni script/report: Train 2020-2023 / OOS 2024-2025
- Split definitivo dichiarato: Train 2020 / OOS 2021-2025

- Execution layer: possibile MetaTrader5 o REST API
- Decisione finale sul broker non ancora presa

## Regola per l'assistente
Se un punto e incoerente tra due file, non scegliere in silenzio.
Segnarlo qui, poi chiedere o proporre un allineamento.
