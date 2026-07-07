---
title: Rendicontazione Settimanale 2026-05-25 2026-05-31
type: weekly_report
priority: high
updated: 2026-06-04
---

# Rendicontazione Settimanale del Progetto Bot Ibrido - 2026-05-25 / 2026-05-31

Documento generato automaticamente dal watcher del vault. La struttura segue il template di rendicontazione completo: dashboard generale, registro concetti, ricerca, versioni bot, evidenze quantitative, decisioni e richieste operative.

## Sintesi della settimana
- Eventi tracciati: 0
- File creati: 0
- File modificati: 0
- File eliminati: 0
- Aree piu attive: nessuna modifica rilevata

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
| File nella knowledge base | 196 |

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
- Nessun file critico modificato nelle aree memoria, strategie, backtest o codice.

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
