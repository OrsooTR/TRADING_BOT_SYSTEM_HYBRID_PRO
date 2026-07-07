---
title: Project State
type: project_memory
priority: critical
updated: 2026-07-07
---

# Project State

## Collegamenti
- [[INDEX]]
- [[DECISIONS_LOG]]
- [[DEVELOPMENT_BACKLOG]]
- [[../00_CORE/Vision]]
- [[../03_STRATEGIES/INDEX]]
- [[../04_BACKTEST/INDEX]]

## Che cos'e oggi
Il progetto e un vault Obsidian di ricerca e progettazione per un bot quant ibrido basato su:
- FFT per estrarre cicli e filtrare rumore
- derivate per timing e direzione
- pattern frattali per struttura multiscala e proiezione
- un motore decisionale che combina segnali e risk management

Oggi il progetto non e ancora un bot eseguibile. E soprattutto una knowledge base con una pipeline di ricerca ben definita.

## Cosa e gia maturo
- visione del sistema e roadmap generale
- filosofia di test: un concetto alla volta, poi combinazione
- 10 moduli validati: 9 concetti standalone + Volatility Regime Gate come meta-filtro di regime
- classifica robustezza consolidata (RSI > Fractal > VWAP > Derivate > EMA Ribbon > BB > ATR > MA)
- integrazione nel vault della linea teorica Pythagoras
- metodologia Train: 2020 (1yr) / OOS: 2021-2025 (5yr) - confermata come standard definitivo il 2026-05-08
- grid search con filtro sessione (all/london/newyork/asian) - novita dalla sessione 2026-05-07
- il compendium 206p ha reso esplicito il layer FFT come pipeline: baseline, regime, confluenza, no-trade logic

## Cosa e ancora incompleto
- implementazione codice del sistema
- pipeline dati riproducibile nel vault
- specifica tecnica completa della logica FFT
- specifica tecnica del pattern layer frattale
- decision engine con formule e regole non ambigue
- execution layer reale con broker, ordini e gestione errori

## Stato delle strategie
- MA Crossover: testato, insight utile come regime filter, non sufficiente come entry standalone
- Derivate 1/2 ordine: testato, PF 2.70 su M5, segnale momentum forte
- RSI Mean-Reversion: testato, 77% profittevoli, piu robusto
- BB Squeeze: testato, edge debole, utile come filtro regime
- Fractal S/R Bounce: testato, 68% profittevoli, precision entry M1
- VWAP Trend Trading: testato, 68% profittevoli M1, bias giornaliero
- ATR Channel Breakout: testato (2026-05-07), 10% profittevoli M15, debole - regime filter
- EMA Ribbon Direction: testato (2026-05-07), 30% profittevoli M15, filtro direzionale London
- FFT Dominant Cycle: testato (2026-05-07), 52% profittevoli M15, London N=256 - prerequisito validato per Layer FFT
- Volatility Regime Gate: testato (2026-05-08), forte su RSI low-vol, moderato su Derivate high-vol - primo meta-filtro validato
- FFT Cycle Prediction: concetto centrale del bot, ancora non validato nel vault
- Fractal FFT Pattern Projection: nuova idea candidata, non ancora implementata

## ⚠️ Rigenerazione 2026-07-07 con motore corretto
La code review del 2026-07-07 ([[../09_LOGS/code_review_2026-07-07]]) ha rivelato che i PF
storici erano gonfiati (tie-break TP/SL ottimistico) e le sessioni shiftate di 5h (fuso EST).
Le 8 famiglie vettoriali sono state rigenerate con motore onesto (spread 0.5 pip, tie
pessimistico, timeout mark-to-market) — numeri e lettura in
[[../09_LOGS/report_giornata_2026-07-07]]. Sintesi:
- le entry standalone su M1/M5 muoiono coi costi (PF < 1), la classifica di robustezza
  storica non è più affidabile
- reggono i **filtri di contesto su M15**: Regime FFT su RSI (PF 1.22), Volatility Gate
  RSI low-vol (delta PF +2.78 M15) e soprattutto **Confluence #17: PF OOS 2.19, DD 5.2%**
- caveat #17: ~9 trade/anno, sotto il criterio >50/anno → da allargare prima della promozione
- le note TESTED restano coi numeri storici finché non vengono riscritte

## Priorita operativa aggiornata
- completare `#12 FFT Spectral Regime Classifier` come primo modulo FFT di regime
- introdurre `#16 Jump / Spike Filter` come secondo meta-filtro
- poi costruire `#17 FFT + Derivative Confluence` come primo ibrido vero
- mantenere Butterworth (#13) come confronto tecnico di filtraggio, non come priorita assoluta di entry

## Architettura attesa del bot finale
1. Data Layer
2. Transform Layer con FFT
3. Pattern Layer frattale
4. Feature Layer
5. Decision Engine
6. Backtest e metriche
7. Logging e miglioramento continuo

## Conclusione operativa
La priorita non e fare live trading subito.
La priorita e rendere riproducibile la ricerca, trasformare il vault in una base di sviluppo concreta e tradurre la teoria frattale in test numerici.
