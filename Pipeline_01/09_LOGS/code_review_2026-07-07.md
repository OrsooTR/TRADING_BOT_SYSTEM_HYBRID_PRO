---
title: Code Review completa
type: log
priority: critical
updated: 2026-07-07
---

# Code Review completa — 2026-07-07

Revisione sistematica di tutto il codice Python (`scripts/` + `src/`). Bug ad alta severità
**corretti** nel codice; i risultati storici in `artifacts/` restano quelli vecchi e vanno
rigenerati prima di essere considerati affidabili.

## Collegamenti
- [[../11_MEMORY/PROJECT_STATE]]
- [[../11_MEMORY/DEVELOPMENT_BACKLOG]]
- [[../04_BACKTEST/INDEX]]

## Bug ad alta severità — CORRETTI

### 1. Tie-break TP/SL ottimistico (tutti gli 8 simulatori vettoriali)
Quando TP e SL venivano colpiti nella **stessa barra** (frequente su M1/M5 con SL 1.0×ATR
e RR≥2), il trade era contato come vincita `+RR` invece che come la più probabile perdita `-1R`.
Questo **gonfiava sistematicamente PF e win-rate** di tutti i risultati in `artifacts/`.
Corretto in pessimistico (pareggio = stop loss) in: `run_atr_vectorized`, `run_ribbon_vectorized`,
`run_fft_cycle_vectorized`, `run_clock_filter`, `run_confluence`, `run_fractal_fft`,
`run_regime_classifier`, `run_volatility_regime_gate_vectorized`.
Nota: il port QuantConnect risolveva già il pareggio in modo pessimistico — le due
implementazioni ora sono coerenti.

### 2. Bug timezone nelle sessioni (tutti i grid script + session_vwap)
I timestamp HistData sono **EST (GMT-5, senza DST)**, ma le finestre di sessione
(`london 7-16`, `newyork 13-21`, `asian 0-8`) erano ore UTC applicate direttamente.
Risultato: "london" selezionava in realtà la sessione di New York, "asian" la mattina di
Londra, ecc. **Tutte le classifiche per sessione nei report storici attribuiscono l'edge
alla sessione sbagliata** (shift di ~5 ore). Corretto con shift `(hour+5)%24` in tutte le
`smask()` e in `session_vwap.py`.

### 3. "Forward returns" del Test A erano rendimenti PASSATI (`run_regime_classifier.py`)
`np.convolve(...,'full')[:T]` calcolava il rendimento delle h barre **precedenti** (le stesse
da cui era calcolato il regime), non delle successive: la validazione del classifier era
circolare e senza valore. Corretto: `fwd[i]` = somma dei log-return da `i+1` a `i+h`;
`regime_test_a_forward_returns.csv` va rigenerato.

### 4. Report con split Train/OOS sbagliato
Docstring e report generati dichiaravano "Train: 2020-2023 | OOS: 2024-2025" mentre il codice
usa **Train: 2020 | OOS: 2021-2025**. Corretto il testo (i report .md storici in artifacts
riportano ancora la dicitura errata finché non vengono rigenerati).

### 5. Path hardcoded di altre macchine (12 script non eseguibili)
7 script puntavano a `/mnt/user-data/uploads/` e `/home/claude/` (sandbox Linux), 5 a
`C:\Users\Ciruzz\` (altro PC). Ora tutti i path sono relativi alla root del repo, con
override via variabile d'ambiente `HISTDATA_DIR` per gli zip HistData
(default: `data/histdata/`). Rimosso anche il salvataggio Excel extra in
`C:\Users\Ciruzz\Downloads` che faceva crashare `run_derivatives_full.py` a fine run.

### 6. Import `derivatives_bt` rotti
4 script importavano `derivatives_bt` senza aggiungere `src/` a `sys.path`
(→ `ModuleNotFoundError`). Corretto.

### 7. Timezone mismatch nel vault reporter
Gli eventi erano timbrati in UTC naive ma i confini settimanali calcolati in ora locale:
gli eventi delle ultime ~2 ore di domenica finivano nella settimana sbagliata. Uniformato.

## Problemi noti APERTI (media severità — da sistemare prima del primo ibrido)

1. **Trade in timeout contati come 0R** — un trade che non tocca né TP né SL entro
   `max_hold` sparisce dal PnL invece di essere chiuso mark-to-market.
2. **Trade sovrapposti compostati come sequenziali** — i simulatori vettoriali non
   de-sovrappongono i segnali: `pnl_pct` e `max_drawdown_pct` sottostimano il rischio
   (il PF non è impattato). Il motore backtrader in `src/derivatives_bt` è invece corretto
   (una posizione alla volta) — i due motori non sono direttamente confrontabili.
3. **Nessuno spread/slippage nei simulatori vettoriali** — fill a costo zero.
4. **Look-ahead nel flag di fine sessione** (`session_vwap.py`) — l'ultima barra di sessione
   è marcata usando il conteggio totale barre della sessione (informazione futura nei giorni
   irregolari).
5. **Cache non invalidate** — `run_fft_clock_filter_grid` riusa il `.pkl` delle feature FFT
   senza verificare che le spec siano cambiate; idem la cache CSV di `run_derivatives_full`.
6. **Persistence window del port QuantConnect** basata sulle valutazioni, non sulle barre
   (diverge dalla definizione di ricerca quando c'è una posizione aperta); sizing su
   `initial_cash` invece che sull'equity corrente.
7. **Codice duplicato 7 volte** — `load_m1`, `resample`, `smask`, `calc_atr`, `calc_ema`,
   `sim_and_metrics`, `build_combined` sono copia-incollati in ogni grid script con piccole
   divergenze. Da centralizzare in `src/` (è il motivo per cui il bug #1 esisteva in 8 copie).
8. **`src/fft_bt/fft_signal.py` è codice morto** — nessuno lo importa.
9. Minori: seed Wilder RSI/ATR senza warmup SMA, `np.roll` che wrappa sul primo bar,
   duplicazione ultima barra in `np.clip` degli orizzonti, `trade_reduction_pct` di
   `run_confluence` calcolato sulla popolazione sbagliata.

## Conseguenza operativa

⚠️ **I numeri storici in `artifacts/` (PF, win-rate, classifiche di sessione) sono
sovrastimati/mal attribuiti** per via dei bug #1 e #2. Prima di costruire l'ibrido #17:
1. rigenerare i backtest dei moduli chiave (#02 Derivate, #03 RSI, #15 Volatility Gate)
   con il codice corretto;
2. riverificare la classifica di robustezza in [[../11_MEMORY/PROJECT_STATE]];
3. aggiornare le note TESTED con i numeri nuovi.
