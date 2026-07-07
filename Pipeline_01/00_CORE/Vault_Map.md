---
title: Vault Map
type: vault_map
priority: critical
updated: 2026-04-29
---

# Vault Map

## Principio organizzativo

Il vault e organizzato come una pipeline di ricerca quant: visione, teoria, dati, strategie, backtest, metriche, decision engine, esecuzione, log, memoria, codice, fonti e artifact.

## Struttura

| Cartella | Ruolo | Cosa ci va |
|----------|-------|------------|
| `00_CORE` | Sistema | Visione, roadmap, regole, mappa del vault |
| `01_THEORY` | Ricerca teorica | FFT, derivate, frattali, pattern |
| `02_DATA` | Dati | Dataset disponibili, pipeline di pulizia, convenzioni |
| `03_STRATEGIES` | Strategie | Idee candidate, strategie testate, template |
| `04_BACKTEST` | Validazione | Template, report linkati, indici dei test |
| `05_METRICS` | Valutazione | Win rate, Sharpe, drawdown, PF, robustezza |
| `06_AGENT_LOGIC` | Decisione | Regole del decision engine |
| `07_AUTOMATION` | Automazioni | Istruzioni Codex, memoria automatica, sync |
| `08_EXECUTION` | Esecuzione | Broker, risk management, ordini |
| `09_LOGS` | Diario | Report giornalieri, esperimenti, note operative |
| `10_DASHBOARD` | Interfaccia | Struttura dashboard e viste operative |
| `11_MEMORY` | Memoria progetto | Stato, decisioni, backlog, research queue, protocollo esperimenti |
| `12_CODE` | Codice documentato | Indici e documentazione dei moduli Python |
| `13_PDF_LIBRARY` | PDF | Mappa markdown -> PDF companion |
| `14_COMPENDIUM` | Compendio | Versione estesa e capitoli del compendio tecnico |
| `15_ARTIFACTS` | Output generati | Indici verso report, dati e workbook in `artifacts` |
| `99_INBOX` | Transito | Note temporanee non ancora classificate |

## Radice del progetto

La radice non e solo vault Obsidian: contiene anche codice e artifact.

| Cartella root | Regola |
|---------------|--------|
| `Pipeline_01` | Knowledge base principale |
| `src` | Codice Python importabile |
| `scripts` | Runner e utility operative |
| `artifacts` | Output generati da backtest e report |
| `assets` | Asset e fonti esterne |
| `.obsidian` | Configurazione Obsidian |
| `node_modules` | Dipendenze tecniche, da ignorare in Obsidian |

## Convenzioni

- Ogni sezione importante deve avere un `INDEX.md`.
- Le note operative giornaliere vanno in `09_LOGS`.
- Le decisioni durevoli vanno in `11_MEMORY/DECISIONS_LOG.md`.
- Le ipotesi future e la coda di ricerca vanno in `11_MEMORY/RESEARCH_QUEUE/`.
- Le strategie nuove partono da `03_STRATEGIES/IDEAS`.
- Le strategie validate passano a `03_STRATEGIES/TESTED`.
- I report generati restano in `artifacts`, ma sono raggiungibili da `15_ARTIFACTS`.
- La documentazione del codice vive in `12_CODE`; il codice eseguibile resta in `src` e `scripts`.
- Le fonti accademiche importate vanno mappate in `13_PDF_LIBRARY/academic_sources.md` e sintetizzate nella sezione teorica corretta.

## Pulizia periodica

1. Svuotare `99_INBOX` spostando ogni nota nella sezione corretta.
2. Aggiornare `11_MEMORY/PROJECT_STATE.md` dopo ogni blocco di lavoro importante.
3. Aggiornare `03_STRATEGIES/INDEX.md` quando una strategia cambia stato.
4. Aggiornare `04_BACKTEST/INDEX.md` quando nasce un nuovo report.
5. Rigenerare la PDF library solo dopo modifiche strutturali importanti.
