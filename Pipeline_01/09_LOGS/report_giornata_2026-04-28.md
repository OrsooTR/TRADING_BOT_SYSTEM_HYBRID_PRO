# Report Giornata — 2026-04-28

## Collegamenti
- [[../00_CORE/00_Regole_Progettazione]]
- [[../03_STRATEGIES/TESTED/03_RSI_MeanReversion]]
- [[../03_STRATEGIES/TESTED/04_BB_Squeeze]]
- [[../03_STRATEGIES/INDEX]]

## Attività svolte

### 1. Backtest Bollinger Band Squeeze + Breakout
- 720 test eseguiti su M1/M5/M15
- Dati: EURUSD 2020-2025 (6 anni)
- Parametri variati: BB Period (10,14,20,30), StdDev (1.5,2.0,2.5), Squeeze %ile (10-30°), RR (2:1–4:1)
- **Best result**: M15 | BB=20 | Std=2.5 | Squeeze=25° | RR=4 → PF 1.22

### 2. Aggiornamento Excel
- Aggiunti fogli: BB_SUMMARY, BB_ALL, BB_M1/M5/M15
- Aggiunto foglio STRATEGY_DESCRIPTIONS (logica, trigger, SL/TP per tutti i 4 concetti)
- Aggiunto foglio GAUSSIAN_ANALYSIS (grafici gaussiani per parametro, tutti i 4 concetti)

### 3. Aggiornamento Vault Obsidian
- Creato [[../03_STRATEGIES/TESTED/04_BB_Squeeze]]
- Creato [[../03_STRATEGIES/TESTED/03_RSI_MeanReversion]] (mancante)
- Aggiornato [[../03_STRATEGIES/INDEX]] con classifica robustezza
- Aggiornato [[../00_CORE/00_Regole_Progettazione]] checkboxes

## Decisioni chiave
- BB Squeeze = edge debole standalone, valore come filtro regime
- RSI Mean-Rev confermato come concetto più robusto (77% profittevoli)
- Derivate 1°/2° = best PF (2.70) su M5

## Prossimo step
- [ ] Backtest ATR Channel Breakout
- [ ] Analisi mega_compendium.pdf (458 pagine)
- [ ] Iniziare test FFT (la base del sistema)

---

## Update sessione pomeriggio

### Backtest Fractal S/R Bounce completato
- 216 test (M1/M5/M15), 146 profittevoli (68%)
- Best: M1 fp=5 tol=0.3 lb=30 rr=3 → PF 1.18, WR 28%
- Nuovo file: [[../03_STRATEGIES/TESTED/05_Fractal_SR_Bounce]]
- Excel aggiornato con fogli FRAC_*
