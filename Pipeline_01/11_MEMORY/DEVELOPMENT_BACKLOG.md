---
title: Development Backlog
type: project_memory
priority: high
updated: 2026-05-08
---

# Development Backlog

## Collegamenti
- [[INDEX]]
- [[PROJECT_STATE]]
- [[DECISIONS_LOG]]
- [[../04_BACKTEST/INDEX]]
- [[../00_CORE/00_Regole_Progettazione]]

## Stato attuale
10 moduli validati: 9 concetti standalone + 1 meta-filtro di regime (#15 Volatility Regime Gate). Prossima fase: Layer FFT e filtri residui prima del primo ibrido multi-layer.
Pipeline completa: `Regime Filter (FFT) -> Entry Signal (Derivate) -> Conviction (Frattali) -> Execution`

---

## Backlog ordinato per priorita

### PRIORITA 1 - Regime e filtri del layer FFT
Testare in sequenza: ognuno prepara il primo ibrido #17.

**#12 - FFT Spectral Regime Classifier**
- Classificare regime da distribuzione energia spettrale
- Da applicare come meta-filtro su #02 (Derivate) e #03 (RSI)
- File idea: [[../03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]
- Prerequisito: #11 completato

**#15 - Volatility Regime Gate**
- Completato il 2026-05-08 con runner vettoriale
- Validato: forte su `RSI + low vol`, moderato su `Derivate + high vol`
- Nota testata: [[../03_STRATEGIES/TESTED/15_Volatility_Regime_Gate]]

**#16 - Jump / Spike Filter**
- Escludere barre Merton-style (rendimento > N x ATR)
- Da applicare come filtro sulle strategie esistenti
- File idea: [[../03_STRATEGIES/IDEAS/jump_spike_filter]]

**#14 - FFT Clock Trigger HFT Filter**
- Picchi spettrali su frequenze calendario -> ridurre size o bloccare trade
- File idea: [[../03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]

### PRIORITA 2 - Primo ibrido operativo

**#17 - FFT + Derivative Confluence**
- Primo ibrido multi-layer: #11 (contesto) + #02 (timing)
- Prerequisiti: #12 e #16; #15 gia validato in forma base
- File idea: [[../03_STRATEGIES/IDEAS/fft_derivative_confluence]]

### PRIORITA 3 - Estensioni e confronto tecnico

**#13 - Butterworth Filter as Trend Signal**
- Sostituto dell'EMA con risposta piatta in banda passante
- Confronto diretto con EMA Ribbon (#08) e filtri FFT
- File idea: [[../03_STRATEGIES/IDEAS/butterworth_trend_filter]]
- Implementazione: scipy.signal.butter + sosfilt

**#09 - Session Time Cluster**
- Mappare edge per fascia oraria UTC
- Semplice, informativo per tutte le strategie successive
- File idea: [[../03_STRATEGIES/IDEAS/session_time_cluster]]

### PRIORITA 4 - Confluenze avanzate

**#18 - Fractal + FFT Confluence**
- Layer geometrico: #07 (frattali) + #11 (ciclo) + #02 (derivate)
- Prerequisiti: #11, #12 e #17; #07 gia validato (PF 1.18 M1)
- File idea: [[../03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]

**#19 - FFT Regime + Strategy Routing**
- Il classifier #12 indirizza il segnale alla strategia ottimale per regime
- Prerequisiti: #12 testato + almeno 2 strategie per regime validati

### PRIORITA 5 - Ricerca avanzata (fase finale)

**#20 - Seasonal ECM Exogenous Signal**
- [[../03_STRATEGIES/IDEAS/seasonal_ecm_exogenous_signal]]

**#21 - Momentum Volume Lifecycle**
- [[../03_STRATEGIES/IDEAS/momentum_volume_lifecycle]]

**#22 - FFT Trend Following**
- [[../03_STRATEGIES/IDEAS/fft_trend_following]]

---

## Note tecniche pendenti

### Pipeline dati
- Formato input OHLC standard: gia operativo con HistData M1 zip
- Pulizia: duplicati, gap, timezone -> gia gestiti in data_utils.py
- Feature layer per FFT: da implementare in forma modulare e riusabile

### FFT implementation checklist
- [ ] Applicare su log-return, non sul prezzo assoluto
- [ ] Costruire baseline strutturale di sessione/calendario prima di leggere i picchi
- [ ] Window function (Hann) obbligatoria per ridurre leakage
- [ ] Parametri finestra (N): testare 64, 128, 256 barre
- [ ] Distinguere banda trend / ciclo / rumore / dead space
- [ ] `dominant_power_ratio` come filtro di qualita del segnale
- [ ] Peak persistence rolling (stabile su train e OOS)
- [ ] No-trade logic esplicita quando il regime e ambiguo o il consenso e insufficiente
- [ ] Sensitivity check su N, bande e soglie
- [ ] Walk-forward o stabilita per finestra prima della promozione finale

### Metriche di accettazione (da Regole_Progettazione)
- PF > 1.3
- DD < 12%
- Trade/anno > 50
- OOS degradation < 40%
