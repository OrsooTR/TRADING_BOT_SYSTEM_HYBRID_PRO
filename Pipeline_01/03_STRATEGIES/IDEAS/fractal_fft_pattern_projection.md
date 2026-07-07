---
title: Fractal + FFT Confluence
type: strategy_idea
status: da_testare
priority: medium
numero: 18
source: compendium_cap_15
---

# 18 — Fractal + FFT Confluence (ex Fractal FFT Pattern Projection)

## Collegamenti
- [[../INDEX]]
- [[../../01_THEORY/FRACTALS/teoria_base]]
- [[../../01_THEORY/FRACTALS/pattern_library]]
- [[../../01_THEORY/FRACTALS/pythagoras_document_analysis]]
- [[../../01_THEORY/FFT/applicazione_trading]]
- [[../../01_THEORY/DERIVATES/derivata_prima]]
- [[../../06_AGENT_LOGIC/decision_system]]

## Idea
Usare pattern frattali multiscala come struttura primaria, FFT come filtro e conferma ciclica, derivate come timing di ingresso.

## Logica
1. selezionare una finestra candidata
2. normalizzare il segmento prezzo-tempo
3. cercare match con una libreria di pattern
4. applicare FFT per isolare componenti dominanti e rumore
5. usare `d1` e `d2` per capire se il pattern sta entrando nella fase operativa
6. generare uno scenario con target, orizzonte temporale e invalidazione

## Output attesi
- `pattern_id`
- `pattern_match_score`
- `pattern_direction`
- `pattern_complexity`
- `fft_cycle_score`
- `d1`
- `d2`
- `target_zone`
- `time_horizon`
- `confidence_score`

## Modalita operative
### Automatic mode
- selezione asset e timeframe
- detection automatica del pattern
- generazione scenario

### Manual mode
- selezione manuale della finestra o del pattern
- confronto con la libreria
- scenario guidato per studio e validazione

## Parametri critici
- finestra di osservazione
- metodo di normalizzazione
- cutoff FFT
- soglia minima di similarita
- definizione dei pivot
- regole di invalidazione

## Primo esperimento minimo
- un solo asset
- un solo timeframe
- un solo pattern semplice
- conferma con `d1` e `d2`
- report IS/OOS separato

## Rischi
- pattern matching troppo discrezionale
- lookahead bias nella scelta della finestra
- overfitting sul template
- eccesso di fiducia nella similitudine visiva

## Nota
Questa idea rappresenta il ponte tra il materiale Pythagoras e una pipeline testabile nel vault.

## Prerequisiti
- [x] #07 Fractal S/R Bounce testato (PF 1.18 M1, 68% profittevoli)
- [ ] #11 FFT Dominant Cycle testato
- [ ] #12 FFT Spectral Regime Classifier testato

## Relazione con altri concetti
- Terzo layer di confluenza dopo [[fft_derivative_confluence]] (#17)
- Rappresenta l'architettura completa del bot: FFT + Derivate + Frattali
