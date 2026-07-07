---
title: Report Giornata 2026-05-08
type: log
priority: medium
updated: 2026-05-08
---

# Report Giornata - 2026-05-08

## Collegamenti
- [[../00_CORE/00_Regole_Progettazione]]
- [[../11_MEMORY/PROJECT_STATE]]
- [[../11_MEMORY/DECISIONS_LOG]]
- [[../11_MEMORY/DEVELOPMENT_BACKLOG]]
- [[../03_STRATEGIES/INDEX]]

## Attivita svolte

### 1. Split standard confermato
- Decisione definitiva: `Train: 2020 | OOS: 2021-2025`
- Lo split e stato trattato come regola fissa del progetto, non piu come scelta aperta

### 2. Analisi checklist dopo il compendium
- Riletta la checklist in [[../00_CORE/00_Regole_Progettazione]]
- Analizzato il compendium tecnico da 206 pagine come guida per il layer Fourier
- Chiarita la lettura corretta: FFT come filtro di contesto/regime prima che come trigger standalone

### 3. Idee applicate al vault
- Aggiunta una `Checklist tecnica FFT` in [[../00_CORE/00_Regole_Progettazione]]
- Formalizzati tre gate emersi dal compendium:
  - baseline strutturale di sessione/calendario
  - no-trade logic
  - sensitivity / walk-forward / controllo overfitting
- Priorita aggiornata: `#12 -> #15 -> #16 -> #17`, con `#13` come confronto tecnico

## Decisioni chiave
- Il primo ibrido da privilegiare e `#17 FFT + Derivative Confluence`
- `#12 FFT Spectral Regime Classifier` e il prossimo modulo strutturale del progetto
- Butterworth resta utile, ma come confronto tecnico di filtraggio piu che come prima milestone del bot

## Implicazione pratica
La checklist non va piu letta come lista di strategie separate.
Va letta come costruzione progressiva del motore ibrido:
`FFT -> regime -> filtri -> confluenza -> execution`

## 4. Backtest eseguito - #15 Volatility Regime Gate
- Implementato un runner vettoriale `pandas + numpy`
- Dataset: EURUSD HistData M1 2020-2025
- Split applicato: `Train 2020 | OOS 2021-2025`
- Test diretto su:
  - RSI Mean-Reversion in regime `low vol`
  - Derivate 1/2 ordine in regime `high vol`
- Aggiunta vista `robust` con soglia minima trade per evitare classifiche distorte da pochi eventi

## Risultato sintetico del backtest
- `RSI + low vol gate` validato con forza
- `Derivate + high vol gate` migliorato ma in modo molto piu modesto
- Decisione: `#15` passa tra i moduli validati del progetto
- Prossimo confronto naturale: `#12 FFT Spectral Regime Classifier`
