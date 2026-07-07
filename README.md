# Trading Bot System — Hybrid Pro

![CI](https://github.com/OrsooTR/TRADING_BOT_SYSTEM_HYBRID_PRO/actions/workflows/ci.yml/badge.svg)
![Pages](https://github.com/OrsooTR/TRADING_BOT_SYSTEM_HYBRID_PRO/actions/workflows/deploy-pages.yml/badge.svg)

Vault di ricerca e sviluppo per un bot di trading quant ibrido basato su **FFT** (cicli e regime),
**derivate** (timing e direzione) e **pattern frattali** (struttura multiscala), con motore
decisionale e risk management.

**📊 Dashboard live:** https://orsootr.github.io/TRADING_BOT_SYSTEM_HYBRID_PRO/

## Struttura

| Cartella | Contenuto |
|---|---|
| `Pipeline_01/` | Vault Obsidian: teoria, strategie, backtest, memoria di progetto, compendium |
| `scripts/` | Runner di backtest vettoriali (pandas/numpy), reporter e utility |
| `src/` | Moduli Python riusabili (`derivatives_bt`, `fft_bt`) |
| `artifacts/` | Output generati: risultati backtest (CSV/JSON) e report |
| `docs/` | Dashboard statica deployata su GitHub Pages |
| `tradingview/` | Indicatori Pine Script |

Punto di ingresso della conoscenza: [START_HERE.md](START_HERE.md).

## Stato del progetto

10 moduli validati (9 strategie standalone + 1 meta-filtro di regime).
Metodologia: Train 2020 / OOS 2021–2025 su EURUSD HistData M1 (resample M1/M5/M15).
Criteri di accettazione: PF > 1.3, DD < 12%, trade/anno > 50, degradazione OOS < 40%.

Stato dettagliato: [PROJECT_STATE](Pipeline_01/11_MEMORY/PROJECT_STATE.md) ·
Backlog: [DEVELOPMENT_BACKLOG](Pipeline_01/11_MEMORY/DEVELOPMENT_BACKLOG.md)

## Dashboard

La dashboard in `docs/` mostra: KPI del progetto, torte per categorie e stato strategie,
**confronto multi-metrica tra strategie** (PF/win rate/DD/trade del best setup OOS +
robustezza dell'intera griglia), **scatter di ottimizzazione** (PF vs ogni parametro e
frontiera rischio/rendimento, per individuare le combinazioni migliori), stato backtest,
file recenti e attività GitHub (live API + feed di build come fallback anti rate-limit).

Il motore vettoriale applica: tie-break TP/SL pessimistico, spread configurabile
(`SPREAD_PIP`, default 0.5 pip), chiusura mark-to-market dei trade in timeout e sessioni
corrette per il fuso EST di HistData. Smoke test: `python tests/test_smoke.py` (eseguito
in CI ad ogni push).

Le statistiche (`docs/data/stats.json`) vengono rigenerate **ad ogni push** e una volta al
giorno dal workflow [deploy-pages.yml](.github/workflows/deploy-pages.yml). In locale:

```bash
python scripts/generate_dashboard_stats.py
```

## Nota sui dati

I CSV di mercato grezzi (>100 MB, es. `eurusd_m1_2020_2025_combined.csv`) **non sono nel repo**
(limite GitHub). Vanno rigenerati/scaricati da HistData e posizionati in
`artifacts/derivative_backtests/data/` e `artifacts/vwap_backtests/data/`.
