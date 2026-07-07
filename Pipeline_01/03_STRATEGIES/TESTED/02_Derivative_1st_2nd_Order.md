# 02 - Derivative 1st and 2nd Order

## Collegamenti
- [[../INDEX]]
- [[../../01_THEORY/DERIVATES/derivata_prima]]
- [[../../04_BACKTEST/INDEX]]
- [[../../06_AGENT_LOGIC/decision_system]]
- [[../../12_CODE/INDEX]]
- [[../../../artifacts/derivative_backtests/reports/derivatives_report_all_tfs_smoke]]
- [[../../../artifacts/derivative_backtests/reports/derivatives_report_m15_full]]

## Obiettivo
Testare un concetto pre-FFT basato solo su derivata prima e derivata seconda.

## Logica
- prezzo base: EMA del close
- `d1 = variazione EMA normalizzata su ATR`
- `d2 = variazione di d1`
- ingresso long: cross positivo di `d1` sopra soglia con `d2` positiva
- ingresso short: cross negativo di `d1` sotto soglia con `d2` negativa

## Risk model
- stop loss su ATR
- take profit con RR variabile
- no pyramiding
- una sola posizione aperta alla volta

## Stato
- base tecnica implementata in codice
- smoke test completato
- run full M15 presente
- grid completa multi-timeframe rimandata alla prossima sessione

## Codice Collegato
- [[../../../src/derivatives_bt/backtest]]
- [[../../../src/derivatives_bt/data_utils]]
- [[../../../scripts/run_derivative_grid]]

## Nota
Questa strategia serve per capire se il blocco `d1 + d2` merita di restare tra i concetti candidati prima della fase FFT.
