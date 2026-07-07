# Log Esperimenti

## Collegamenti
- [[INDEX]]
- [[report_giornata_2026-04-22]]
- [[../04_BACKTEST/INDEX]]
- [[../03_STRATEGIES/TESTED/01_MA_Crossover]]
- [[../03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]

## Formato
- data
- test
- risultato
- miglioramento
- decisione successiva

## Sessioni collegate
- [[report_giornata_2026-04-22]]
- [[../../artifacts/derivative_backtests/reports/derivatives_report_all_tfs_smoke]]
- [[../../artifacts/derivative_backtests/reports/derivatives_report_m15_full]]
- [[report_giornata_2026-05-08]]
- [[../../artifacts/volatility_gate_backtests/reports/volatility_gate_report_all_robust]]

## 2026-05-08 - Volatility Regime Gate (#15)
- test: gate di volatilita ATR-based su RSI e Derivate con split `Train 2020 | OOS 2021-2025`
- risultato: forte miglioramento su `RSI + low vol`, miglioramento piccolo ma reale su `Derivate + high vol`
- miglioramento: introdotta vista robust con soglia minima trade per evitare ranking falsati da pochi trade
- decisione successiva: procedere con `#12 FFT Spectral Regime Classifier` e poi `#16 Jump / Spike Filter`
