---
title: "Compendio tecnico - Hub principale"
tags:
  - indice
  - navigazione
  - compendio
---

# Compendio tecnico del sistema trading ibrido

> **Fonte:** `TRADING_BOT_COMPENDIUM.pdf` â€” 206 pagine, versione espansa italiana
> **Struttura:** 26 capitoli + 37 appendici formule + 12 casi studio + 16 scenari + 60 schede avanzate

---

## Mappa del sistema

```
Dato grezzo â†’ Pulizia â†’ Decomposizione â†’ Pattern â†’ Decisione â†’ Esecuzione â†’ Misurazione â†’ Apprendimento
```

| Strato | Capitoli chiave |
|--------|----------------|
| **Dati** | [[CAPITOLI/02_Qualita_Dato|2]], [[CAPITOLI/03_Rendimenti|3]], [[CAPITOLI/12_Non_Stazionarieta|12]] |
| **Segnale / Frequenza** | [[CAPITOLI/04_Smoothing|4]], [[CAPITOLI/06_Fourier_Continua|6]], [[CAPITOLI/07_DFT_FFT|7]], [[CAPITOLI/08_Sampling_Nyquist|8]], [[CAPITOLI/09_Butterworth|9]], [[CAPITOLI/10_Wiener_Kolmogorov|10]], [[CAPITOLI/11_Band_Limited|11]] |
| **Derivate** | [[CAPITOLI/05_Derivate|5]] |
| **Frattali** | [[CAPITOLI/13_Frattali_Pattern|13]], [[CAPITOLI/14_Frattali_Operativi|14]] |
| **Confluenza / Regime** | [[CAPITOLI/15_Confluenza|15]], [[CAPITOLI/16_Regime_Detection|16]] |
| **Rischio / Validazione** | [[CAPITOLI/17_Risk_Management|17]], [[CAPITOLI/18_Backtest|18]], [[CAPITOLI/19_Walk_Forward|19]], [[CAPITOLI/20_Metriche|20]] |
| **Pricing** | [[CAPITOLI/21_Pricing_Fourier|21]], [[CAPITOLI/22_Black_Scholes|22]], [[CAPITOLI/23_Merton|23]], [[CAPITOLI/24_Variance_Gamma|24]] |
| **Architettura / Log** | [[CAPITOLI/01_Architettura|1]], [[CAPITOLI/25_Architettura_Bot|25]], [[CAPITOLI/26_Logging_Memoria|26]] |

---

## 26 Capitoli

### Architettura e sistema
- [[CAPITOLI/01_Architettura|1. Architettura generale del sistema ibrido]]
- [[CAPITOLI/25_Architettura_Bot|25. Architettura implementativa del bot e flusso dei moduli]]
- [[CAPITOLI/26_Logging_Memoria|26. Logging, memoria sperimentale e ciclo di apprendimento]]

### Dati e preprocessing
- [[CAPITOLI/02_Qualita_Dato|2. QualitÃ  del dato, preprocessing e integritÃ  del campione]]
- [[CAPITOLI/03_Rendimenti|3. Rendimenti, log-return e distribuzioni empiriche]]
- [[CAPITOLI/12_Non_Stazionarieta|12. Serie non stazionarie, differencing e trend removal]]

### Segnale e frequenza
- [[CAPITOLI/04_Smoothing|4. Smoothing, estrazione del segnale e separazione del residuo]]
- [[CAPITOLI/05_Derivate|5. Derivate discrete, velocitÃ  e accelerazione del prezzo]]
- [[CAPITOLI/06_Fourier_Continua|6. Fourier continua e lettura spettrale del mercato]]
- [[CAPITOLI/07_DFT_FFT|7. DFT, FFT e rappresentazione discreta]]
- [[CAPITOLI/08_Sampling_Nyquist|8. Sampling, Nyquist, aliasing e finestra]]
- [[CAPITOLI/09_Butterworth|9. Filtri Butterworth e separazione in frequenza]]
- [[CAPITOLI/10_Wiener_Kolmogorov|10. Wiener-Kolmogorov e signal extraction ottimale]]
- [[CAPITOLI/11_Band_Limited|11. Processi band-limited e dead spaces spettrali]]

### Frattali e confluenza
- [[CAPITOLI/13_Frattali_Pattern|13. Frattali, pivot e libreria di pattern a candele]]
- [[CAPITOLI/14_Frattali_Operativi|14. Frattali operativi: timing, compressione e breakout]]
- [[CAPITOLI/15_Confluenza|15. Confluenza tra FFT, derivate e frattali]]
- [[CAPITOLI/16_Regime_Detection|16. Regime detection e classificazione dello stato di mercato]]

### Rischio e validazione
- [[CAPITOLI/17_Risk_Management|17. Risk management, size, stop loss e take profit]]
- [[CAPITOLI/18_Backtest|18. Backtest, leakage e architettura di validazione]]
- [[CAPITOLI/19_Walk_Forward|19. Walk-forward, Monte Carlo e robustezza parametrica]]
- [[CAPITOLI/20_Metriche|20. Metriche di performance e diagnostica del sistema]]

### Pricing e modelli stocastici
- [[CAPITOLI/21_Pricing_Fourier|21. Pricing via Fourier e funzione caratteristica]]
- [[CAPITOLI/22_Black_Scholes|22. Black-Scholes, ipotesi forti e valore del caso base]]
- [[CAPITOLI/23_Merton|23. Merton jump-diffusion e mercato con salti]]
- [[CAPITOLI/24_Variance_Gamma|24. Variance Gamma, LÃ©vy e code piÃ¹ realistiche]]

---

## Appendici

| File | Contenuto |
|------|-----------|
| [[APPENDICI/A1_Formule|A1 â€” Formule]] | 37 appendici formula con derivazioni e uso operativo |
| [[APPENDICI/A2_Studi_di_Caso|A2 â€” Studi di caso]] | 12 casi studio su scenari EURUSD reali |
| [[APPENDICI/A3_Scenari_Operativi|A3 â€” Scenari operativi]] | 16 scenari: trend, range, spike, overfitting... |
| [[APPENDICI/A4_Schede_Avanzate|A4 â€” Schede avanzate]] | 60 schede tecniche di approfondimento |

---

## Link al resto del vault

| Sezione | Link |
|---------|------|
| Vision e roadmap | [[../00_CORE/Vision|Vision]], [[../00_CORE/Roadmap|Roadmap]] |
| Teoria | [[../01_THEORY/INDEX|Theory INDEX]] |
| Dati | [[../02_DATA/INDEX|Data INDEX]] |
| Strategie | [[../03_STRATEGIES/INDEX|Strategies INDEX]] |
| Backtest | [[../04_BACKTEST/INDEX|Backtest INDEX]] |
| Metriche | [[../05_METRICS/INDEX|Metrics INDEX]] |
| Agent logic | [[../06_AGENT_LOGIC/decision_system|Decision System]] |
| Esecuzione | [[../08_EXECUTION/INDEX|Execution INDEX]] |
| Log | [[../09_LOGS/INDEX|Logs INDEX]] |
| Memoria | [[../11_MEMORY/INDEX|Memory INDEX]] |
| Codice | [[../12_CODE/INDEX|Code INDEX]] |

---

## Note sui file precedenti

I file `01_Architettura.md` â†’ `12_Glossario.md` nella root di questa cartella
sono la versione precedente del compendio (12 sezioni compresse).
La nuova struttura in `CAPITOLI/` offre granularitÃ  1-a-1 con i 26 capitoli del PDF.
