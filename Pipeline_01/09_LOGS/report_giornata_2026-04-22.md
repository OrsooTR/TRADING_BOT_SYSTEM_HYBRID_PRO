# Report Giornata - 2026-04-22

## Collegamenti
- [[INDEX]]
- [[../11_MEMORY/INDEX]]
- [[../03_STRATEGIES/TESTED/01_MA_Crossover]]
- [[../03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]
- [[../../artifacts/derivative_backtests/reports/derivatives_report_all_tfs_smoke]]
- [[../../artifacts/derivative_backtests/reports/derivatives_report_m15_full]]

## Executive Summary
- Il progetto e stato analizzato e riorganizzato come vault Obsidian con memoria operativa centrale.
- E stata costruita la base tecnica per i backtest sulle derivate con parser HistData, strategia Backtrader e runner di grid search.
- E stato eseguito uno smoke test sulla strategia a derivate; la grid completa e stata preparata ma rimandata a domani.
- Il backtest MA Crossover presente nel workbook resta il riferimento empirico piu maturo della giornata.

## Cosa E Stato Fatto Oggi
- Analisi del progetto e identificazione del suo stato reale: research vault, non bot eseguibile.
- Creazione della sezione `11_MEMORY` per rendere il vault riutilizzabile senza rileggere ogni volta la chat.
- Aggiornamento delle istruzioni di automazione e memory rules.
- Implementazione del modulo `derivatives_bt` con loader dati, strategia e metriche.
- Implementazione del runner di grid search per EUR/USD su M1, M5 e M15.
- Esecuzione di smoke test ridotti e salvataggio dei risultati in `artifacts/derivative_backtests`.

## Backtest MA Crossover Gia Disponibile
- Fonte: `C:\Users\Ciruzz\Downloads\MA_Cross_GridSearch_EURUSD_1.xlsx`
- Miglior configurazione assoluta: M1, MA 50/150, RR 4, PF 1.133, DD 55%, P&L 1018.6%.
- La gerarchia dei risultati conferma che M1 domina, M5 e quasi privo di edge, M15 resta debole.

### Osservazioni Workbook
- 1. M1 domina: PF max 1.13 (50/150 RR4). Compounding su migliaia di trade.
- 2. M5 quasi zero edge. Solo 5/150 RR2 marginale (PF 1.02).
- 3. M15 debole: PF max 1.04 (50/150 RR1, 50/200 RR1). Pochi trade.
- 4. RR alti (3:1, 4:1) sono il driver: WR 20-22% ma vincite 3-4x le perdite.
- 5. Fast MA 50 + Slow MA 150-200 = miglior filtro (meno noise).
- 6. DD resta 45-55% anche nelle migliori → serve position sizing.
- 7. Conclusione: MA cross ha edge su M1 con RR alto e MA lente.

## Stato Derivative Backtest
- Strategia definita su EMA(close), derivata prima normalizzata su ATR e derivata seconda.
- Dataset pronto: EUR/USD M1 HistData 2020-2025 con resampling previsto a M5 e M15.
- Smoke test completato su finestra ridotta per verificare parsing, ordini, SL/TP e metriche.
- Miglior setup smoke: M15 | smooth 5 | d1 2 | d2 2 | RR 3.0 | OOS PF 0.340 | OOS DD 6.38% | OOS P&L -5.55%.
- La grid completa non e stata eseguita oggi; la fase full e stata rimandata a domani.

## File Significativi Creati o Aggiornati
- `Pipeline_01/07_AUTOMATION/codex_instructions.md`
- `Pipeline_01/07_AUTOMATION/memory_rules.md`
- `Pipeline_01/11_MEMORY/INDEX.md`
- `Pipeline_01/11_MEMORY/PROJECT_STATE.md`
- `Pipeline_01/11_MEMORY/DECISIONS_LOG.md`
- `Pipeline_01/11_MEMORY/DEVELOPMENT_BACKLOG.md`
- `Pipeline_01/11_MEMORY/ASSISTANT_CONTEXT.md`
- `Pipeline_01/11_MEMORY/EXPERIMENT_PROTOCOL.md`
- `src/derivatives_bt/data_utils.py`
- `src/derivatives_bt/backtest.py`
- `scripts/run_derivative_grid.py`
- `artifacts/derivative_backtests/data/derivatives_grid_results_smoke.csv`
- `artifacts/derivative_backtests/reports/derivatives_report_all_tfs_smoke.md`

## Priorita Per Domani
- Eseguire la grid completa sulle derivate con multiprocessing fuori sandbox.
- Popolare il workbook Excel con tutti i risultati, buoni e cattivi.
- Aggiornare il vault con report completi M1, M5, M15 e all-timeframe.
- Valutare se la logica d1+d2 abbia edge sufficiente per entrare nel set di concetti candidati pre-FFT.

