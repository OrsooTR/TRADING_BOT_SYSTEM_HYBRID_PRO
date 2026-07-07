---
title: Rendicontazione Settimanale 2026-06-01 2026-06-07
type: weekly_report
priority: high
updated: 2026-06-04
---

# Rendicontazione Settimanale del Progetto Bot Ibrido - 2026-06-01 / 2026-06-07

Documento generato automaticamente dal watcher del vault. La struttura segue il template di rendicontazione completo: dashboard generale, registro concetti, ricerca, versioni bot, evidenze quantitative, decisioni e richieste operative.

## Sintesi della settimana
- Eventi tracciati: 353
- File creati: 349
- File modificati: 4
- File eliminati: 0
- Aree piu attive: artifacts (124), 14_COMPENDIUM (52), 03_STRATEGIES (37), 11_MEMORY (25), 01_THEORY (21)

## 1. Dashboard generale dello stato del progetto
| Area | Stato stimato | Nota operativa |
| --- | --- | --- |
| Infrastruttura dati | 90% | Dataset e cartelle dati presenti nel vault. |
| Motore di backtest | 85% | Runner e report di backtest disponibili in scripts/artifacts. |
| Ricerca FFT | 82% | Layer FFT gia ricorrente nella memoria di progetto. |
| Ricerca Frattali | 72% | Base concettuale presente, da rendere piu numerica. |
| Ricerca Regimi di Mercato | 75% | Meta-filtri e classificatori in avanzamento. |
| Documentazione | 95% | Vault molto ricco e navigabile. |
| Knowledge Base Obsidian | 95% | Struttura Obsidian rilevata e aggiornata. |
| Integrazione Strategie | 65% | Integrazione ancora da consolidare nel bot finale. |
| Decision Engine | 55% | Schema presente, regole finali da congelare. |
| Bot Prototipo | 60% | Prototipi e logica disponibili, produzione non pronta. |
| Paper Trading | 10% | Fase successiva alla validazione. |
| Produzione Live | 0% | Non avviata, coerente con lo stato del progetto. |

## 2. Registro dei concetti testati
| Concetto | Stato | Lettura sintetica |
| --- | --- | --- |
| FFT Dominant Cycle | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/11_FFT_Dominant_Cycle.md |
| FFT Spectral Regime Classifier | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/12_FFT_Spectral_Regime_Classifier.md |
| Volatility Regime Gate | In studio | Idea nel vault: Pipeline_01/03_STRATEGIES/IDEAS/volatility_regime_gate.md |
| 01 - MA Crossover | Scartato | Presente in Pipeline_01/03_STRATEGIES/TESTED/01_MA_Crossover.md |
| 02 - Derivative 1st and 2nd Order | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order.md |
| 03 — RSI Mean-Reversion | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/03_RSI_MeanReversion.md |
| 04 — Bollinger Band Squeeze + Breakout | Testato | Presente in Pipeline_01/03_STRATEGIES/TESTED/04_BB_Squeeze.md |
| 05 — Fractal Support & Resistance Bounce | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/05_Fractal_SR_Bounce.md |
| 06 — VWAP Trend Trading | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/06_VWAP_TrendTrading.md |
| 15 - Volatility Regime Gate | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/15_Volatility_Regime_Gate.md |
| ATR Channel Breakout | Testato | Presente in Pipeline_01/03_STRATEGIES/TESTED/07_ATR_Channel_Breakout.md |
| Butterworth Filter as Trend Signal | In studio | Idea nel vault: Pipeline_01/03_STRATEGIES/IDEAS/butterworth_trend_filter.md |
| EMA Ribbon Direction Filter | Testato | Presente in Pipeline_01/03_STRATEGIES/TESTED/08_EMA_Ribbon_Direction.md |
| FFT + Derivative Confluence | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/17_FFT_Derivative_Confluence.md |
| FFT Clock Trigger HFT Filter | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/14_FFT_Clock_Trigger_HFT_Filter.md |
| Fractal + FFT Confluence | Integrato / promettente | Presente in Pipeline_01/03_STRATEGIES/TESTED/18_Fractal_FFT_Confluence.md |
| Jump / Spike Filter | In studio | Idea nel vault: Pipeline_01/03_STRATEGIES/IDEAS/jump_spike_filter.md |
| Momentum Volume Lifecycle | In studio | Idea nel vault: Pipeline_01/03_STRATEGIES/IDEAS/momentum_volume_lifecycle.md |

## 3. Dashboard della ricerca
| Metrica | Valore |
| --- | --- |
| Concetti analizzati | 18 |
| Concetti testati / integrati | 13 |
| Concetti scartati | 1 |
| Concetti promettenti | 10 |
| Concetti ancora in studio | 4 |
| File nella knowledge base | 197 |

## 4. Dashboard dei bot e delle versioni
| Versione | Stato | Esito | Obiettivo | Lezione chiave |
| --- | --- | --- | --- | --- |
| V1 | Esplorazione iniziale | Storico | Segnali singoli fragili | Serve modularita e filtro di contesto |
| V2 | FFT / ciclo dominante | Promettente | Lettura ritmo mercato | Base per regime classifier |
| V3 | Frattali + S/R | Promettente | Struttura geometrica | Da confermare con ritmo e regime |
| V4 | Hybrid multi-layer | In sviluppo | Regime + ciclo + trigger | Direzione principale del progetto |
| V5 | Bot finale modulare | Prossimo obiettivo | Session-aware e risk-aware | Congelare decision engine |

## 5. Evidenze quantitative standard
| Strategia / report | TF | Profit Factor | Win Rate | Drawdown | Trade | Fonte |
| --- | --- | --- | --- | --- | --- | --- |
| atr backtests/data/atr results all.csv | M15 | 1.4208 | 41.4 | 26.86 | 314 | artifacts/atr_backtests/data/atr_results_all.csv |
| atr backtests/data/atr results m1.csv | M1 | 1.0871 | 21.36 | 90.36 | 9498 | artifacts/atr_backtests/data/atr_results_m1.csv |
| atr backtests/data/atr results m15.csv | M15 | 1.4208 | 41.4 | 26.86 | 314 | artifacts/atr_backtests/data/atr_results_m15.csv |
| atr backtests/data/atr results m5.csv | M5 | 1.0619 | 34.68 | 23.11 | 594 | artifacts/atr_backtests/data/atr_results_m5.csv |
| clock backtests/data/clock results all.csv | M15 | 1.2603 | 38.33 | 19.32 | 120 | artifacts/clock_backtests/data/clock_results_all.csv |
| clock backtests/data/clock results m1.csv | M1 | 1.1329 | 35.98 | 47.53 | 3257 | artifacts/clock_backtests/data/clock_results_m1.csv |
| clock backtests/data/clock results m15.csv | M15 | 1.2603 | 38.33 | 19.32 | 120 | artifacts/clock_backtests/data/clock_results_m15.csv |
| clock backtests/data/clock results m5.csv | M5 | 1.0893 | 35.26 | 25.82 | 709 | artifacts/clock_backtests/data/clock_results_m5.csv |
| confluence backtests/data/confluence resul | M5 | inf | 100.0 | 0.0 | 1 | artifacts/confluence_backtests/data/confluence_results_all.csv |
| confluence backtests/data/confluence resul | M15 | 8.0 | 66.67 | 1.0 | 3 | artifacts/confluence_backtests/data/confluence_results_m15.csv |
| confluence backtests/data/confluence resul | M5 | inf | 100.0 | 0.0 | 1 | artifacts/confluence_backtests/data/confluence_results_m5.csv |
| derivative backtests/data/derivatives grid | M15 | inf | 100.0 | 0.0 | 1 | artifacts/derivative_backtests/data/derivatives_grid_results_full.csv |

## 6. File significativi aggiunti o modificati
- `artifacts/volatility_gate_backtests/reports/volatility_gate_report_derivative.md` - created - Volatility Regime Gate DERIVATIVE; Related Notes; Logic; Best Setup
- `artifacts/volatility_gate_backtests/reports/volatility_gate_report_derivative_robust.md` - created - Volatility Regime Gate DERIVATIVE ROBUST; Related Notes; Logic; Best Setup
- `artifacts/volatility_gate_backtests/reports/volatility_gate_report_rsi.md` - created - Volatility Regime Gate RSI; Related Notes; Logic; Best Setup
- `artifacts/volatility_gate_backtests/reports/volatility_gate_report_rsi_robust.md` - created - Volatility Regime Gate RSI ROBUST; Related Notes; Logic; Best Setup
- `artifacts/vwap_backtests/data/eurusd_m1_2020_2025_combined.csv` - created - datetime,open,high,low,close,volume 2020-01-01 17:00:00,1.1212,1.12121,1.12117,1.1212,0.0 2020-01-01 17:01:00,1.12106,1.12135,1.12106,1.12135,0.0 2020-01-01 17:02:00,1.12136,1.12139,1.12136,1.12139,0.0 2020-01-01 17:03:00,1.12135,1.12135,1.1212,1.12122,0.0
- `artifacts/vwap_backtests/data/run_metadata_smoke.json` - created - { "generated_at": "2026-04-28 09:45:57 UTC", "mode": "smoke", "zip_paths": [ "C:\\Users\\Ciruzz\\Downloads\\Progetto Trading Files\\HISTDATA_COM_ASCII_EURUSD_M12020.zip",
- `artifacts/vwap_backtests/data/vwap_session_results_m1_smoke.csv` - created - tf,session_label,min_session_bars,entry_atr_mult,rejection_frac,sl_atr_mult,rr,train_trades,train_win_rate,train_profit_factor,train_max_drawdown_pct,train_pnl_pct,oos_trades,oos_win_rate,oos_profit_factor,oos_max_drawdown_pct,oos_pnl_pct,total_trades,total_longs,total_shorts,avg_bars M1,day,30,1.5,0.25,1.0,3.0,43,44.18604651162791,1.009613065261364,48.656562259705126,0.9329669692066167,44,47.72727272727273,1.8646989704034413,15.334993790667435,58.95135149138142,87,17,70,594.471264367816 M1,day,
- `artifacts/vwap_backtests/data/vwap_session_results_smoke.csv` - created - tf,session_label,min_session_bars,entry_atr_mult,rejection_frac,sl_atr_mult,rr,train_trades,train_win_rate,train_profit_factor,train_max_drawdown_pct,train_pnl_pct,oos_trades,oos_win_rate,oos_profit_factor,oos_max_drawdown_pct,oos_pnl_pct,total_trades,total_longs,total_shorts,avg_bars M1,day,30,1.5,0.25,1.0,3.0,43,44.18604651162791,1.009613065261364,48.656562259705126,0.9329669692066167,44,47.72727272727273,1.8646989704034413,15.334993790667435,58.95135149138142,87,17,70,594.471264367816 M1,day,
- `artifacts/vwap_backtests/data/vwap_session_results_smoke.json` - created - [ { "tf":"M1", "session_label":"day", "min_session_bars":30,
- `artifacts/vwap_backtests/reports/vwap_session_report_all_tfs_smoke.md` - created - Backtest VWAP Session Mean Reversion EURUSD ALL_TFS; Related Notes; Logic; Best Setup
- `artifacts/vwap_backtests/reports/vwap_session_report_m1_smoke.md` - created - Backtest VWAP Session Mean Reversion EURUSD M1; Related Notes; Logic; Best Setup
- `Pipeline_01/09_LOGS/WEEKLY_REPORTS/rendicontazione_settimanale_2026-06-01_2026-06-07.md` - created - Rendicontazione Settimanale del Progetto Bot Ibrido - 2026-06-01 / 2026-06-07; Sintesi della settimana; 1. Dashboard generale dello stato del progetto; 2. Registro dei concetti testati
- `scripts/vault_weekly_reporter.py` - modified - from __future__ import annotations import argparse import csv import hashlib import html
- `artifacts/vault_reporting/rendicontazione_settimanale_2026-06-01_2026-06-07.pdf` - created - created
- `Pipeline_01/09_LOGS/WEEKLY_REPORTS/rendicontazione_settimanale_2026-06-01_2026-06-07.md` - modified - Rendicontazione Settimanale del Progetto Bot Ibrido - 2026-06-01 / 2026-06-07; Sintesi della settimana; 1. Dashboard generale dello stato del progetto; 2. Registro dei concetti testati
- `scripts/vault_weekly_reporter.py` - modified - from __future__ import annotations import argparse import csv import hashlib import html
- `artifacts/vault_reporting/rendicontazione_settimanale_2026-06-01_2026-06-07.pdf` - modified - modified
- `Pipeline_01/09_LOGS/WEEKLY_REPORTS/rendicontazione_settimanale_2026-05-25_2026-05-31.md` - created - Rendicontazione Settimanale del Progetto Bot Ibrido - 2026-05-25 / 2026-05-31; Sintesi della settimana; 1. Dashboard generale dello stato del progetto; 2. Registro dei concetti testati
- `artifacts/vault_reporting/rendicontazione_settimanale_2026-05-25_2026-05-31.pdf` - created - created
- `artifacts/vault_reporting/reporter_state.json` - created - { "last_weekly_report_start": "2026-05-25", "last_weekly_report_at": "2026-06-04T14:37:21" }

## 7. Decisioni del periodo
- ## Decisioni confermate
- Il sistema va costruito per layer: dati, trasformazioni, feature, decisione, backtest, logging
- Il PDF Pythagoras e piu utile come blueprint di prodotto che come modello matematico gia validato
- Test validato finora: EURUSD con edge migliore su M1
- Decisione finale sul broker non ancora presa
- 10 moduli validati: 9 concetti standalone + 1 meta-filtro di regime (#15 Volatility Regime Gate). Prossima fase: Layer FFT e filtri residui prima del primo ibrido multi-layer.
- ## Backlog ordinato per priorita
- ### PRIORITA 1 - Regime e filtri del layer FFT

## 8. Richieste operative
- Programmatore: alta priorita per modularizzazione, orchestration dei layer e generazione metriche ripetibile.
- Supporto ricerca / AI: alta priorita per sintesi settimanale, pulizia backlog e definizione esperimenti.
- Server dedicato: priorita media, utile quando le grid diventano continue o molto pesanti.

## 9. Roadmap suggerita
- 0-30 giorni: congelare moduli del bot finale, standardizzare log/backtest e mantenere questa rendicontazione attiva.
- 30-60 giorni: integrare strategie per regime e completare il decision engine.
- 60-90 giorni: paper trading controllato, pulizia falsi positivi e consolidamento operativo.

## Conclusione tecnica
La settimana viene misurata non solo come attivita svolta, ma come avanzamento della maturita del sistema. Il watcher mantiene la memoria delle modifiche, mentre il report sintetizza lo stato del laboratorio, le evidenze quantitative e i prossimi passi operativi.
