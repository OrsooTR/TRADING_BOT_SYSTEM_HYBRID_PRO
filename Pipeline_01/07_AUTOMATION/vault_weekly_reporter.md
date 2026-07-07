---
title: Vault Weekly Reporter
type: automation
priority: high
updated: 2026-06-04
---

# Vault Weekly Reporter

Automazione locale per mantenere una memoria continua delle modifiche del vault e generare una rendicontazione settimanale nello stile del template `RENDICONTAZIONE_COMPLETA.pdf`.

## File principali
- `scripts/vault_weekly_reporter.py`: watcher, memoria SQLite, generatore Markdown/PDF.
- `start_vault_weekly_reporter.bat`: launcher continuo in background.
- `run_weekly_report_now.bat`: esegue una scansione e genera subito il report della settimana corrente.
- `install_vault_reporter_autostart.ps1`: installa il watcher all'avvio di Windows tramite Operazioni Pianificate.
- `uninstall_vault_reporter_autostart.ps1`: rimuove l'autostart.

## Output
- Memoria eventi: `artifacts/vault_reporting/vault_memory.sqlite`
- Log tecnico: `artifacts/vault_reporting/vault_weekly_reporter.log`
- Report Markdown: `Pipeline_01/09_LOGS/WEEKLY_REPORTS/`
- Report PDF: `artifacts/vault_reporting/`

## Uso rapido
1. Per generare subito una rendicontazione: eseguire `run_weekly_report_now.bat`.
2. Per avviare il watcher manualmente: eseguire `start_vault_weekly_reporter.bat`.
3. Per installarlo all'avvio del PC: aprire PowerShell nella root del progetto ed eseguire:

```powershell
.\install_vault_reporter_autostart.ps1
```

## Comportamento
- Il watcher scansiona il vault ogni 60 secondi quando il PC e acceso.
- Registra file creati, modificati ed eliminati.
- Mantiene una memoria locale persistente in SQLite.
- Ogni domenica alle 23:30 genera la rendicontazione della settimana corrente.
- Il report segue la struttura: dashboard generale, registro concetti, dashboard ricerca, dashboard bot, evidenze quantitative, decisioni, richieste operative e roadmap.
