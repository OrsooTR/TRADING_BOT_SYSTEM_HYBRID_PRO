# 15 - Volatility Regime Gate

## Collegamenti
- [[../INDEX]]
- [[../IDEAS/volatility_regime_gate]]
- [[../../00_CORE/00_Regole_Progettazione]]
- [[../../04_BACKTEST/INDEX]]
- [[../../11_MEMORY/PROJECT_STATE]]
- [[../../../artifacts/volatility_gate_backtests/reports/volatility_gate_report_all_robust]]
- [[../../../artifacts/volatility_gate_backtests/reports/volatility_gate_report_derivative_robust]]
- [[../../../artifacts/volatility_gate_backtests/reports/volatility_gate_report_rsi_robust]]

## Obiettivo
Testare un meta-filtro di regime basato sulla volatilita relativa, per capire se:
- le strategie mean-reversion migliorano quando operano solo in bassa volatilita
- le strategie momentum migliorano quando operano solo in alta volatilita

## Split e motore
- Train: 2020
- OOS: 2021-2025
- Motore: pandas + numpy vectorized
- Dataset: EURUSD HistData M1, poi resample M1 / M5 / M15

## Implementazione del gate
Per ragioni di velocita e stabilita il percentile ATR e stato implementato come soglia rolling a quantile:

1. ATR(14) su ogni barra
2. soglia rolling su finestre `50 / 100 / 200`
3. `low vol` quando ATR <= quantile basso
4. `high vol` quando ATR >= quantile alto
5. zona intermedia = no trade

Valori testati:
- low vol threshold: `20%`, `30%`
- high vol threshold: `70%`, `80%`

## Strategie base usate

### RSI low-vol
- RSI period: `14`, `21`
- OB/OS: `70/30`, `80/20`
- entry mode: `touch`, `cross`
- SL: `1.5 x ATR`
- RR: `2`, `3`, `4`

### Derivative high-vol
- smooth period: `20`
- d1 period: `4`, `8`
- d2 period: `2`, `4`
- d1 threshold: `0.05`, `0.10`
- d2 threshold: `0.00`
- SL: `1.0`, `1.5`
- RR: `2`, `3`, `4`

## Risultato principale
Il concetto e valido, ma in modo asimmetrico:

- **forte su RSI mean-reversion in low volatility**
- **solo moderatamente utile su Derivate in high volatility**

Quindi `#15` entra tra i moduli validati del progetto, ma con una decisione chiara:
- usare il gate soprattutto per selezionare i contesti mean-reversion
- non considerarlo ancora un moltiplicatore forte del blocco momentum

## Best robust setup - RSI low-vol
- TF: `M5`
- RSI: `14`
- OB/OS: `80 / 20`
- Mode: `touch`
- RR: `2`
- Gate lookback: `200`
- Gate threshold: `0.30`
- OOS base PF: `1.0687`
- OOS gated PF: `1.3973`
- OOS delta PF: `+0.3286`
- OOS trades: `1230 -> 248`
- Trade reduction: `79.84%`

## Best robust setup - Derivative high-vol
- TF: `M15`
- Smooth: `20`
- D1/D2: `4 / 2`
- D1 threshold: `0.10`
- SL ATR: `1.0`
- RR: `2`
- Gate lookback: `200`
- Gate threshold: `0.80`
- OOS base PF: `0.9987`
- OOS gated PF: `1.1028`
- OOS delta PF: `+0.1041`
- OOS trades: `7805 -> 1419`
- Trade reduction: `81.82%`

## Lettura operativa
1. La bassa volatilita seleziona davvero un contesto migliore per RSI.
2. L'alta volatilita migliora Derivate, ma il beneficio e contenuto.
3. Il gate riduce molto i trade, quindi va trattato come filtro di qualita, non come overlay neutro.
4. I risultati migliori robusti restano compatibili con la filosofia del compendium: no-trade zone tra i due regimi.

## Decisione
- `#15 Volatility Regime Gate` = **testato e validato**
- promuovere il ramo `RSI + low vol gate` come baseline per futuri confronti con `#12 FFT Spectral Regime Classifier`
- mantenere `Derivative + high vol gate` come supporto utile ma non ancora decisivo

## Prossimo passo naturale
- confrontare il gate ATR di `#15` con il classifier spettrale di `#12`
- applicare `#16 Jump / Spike Filter` sopra i setup migliori di RSI e Derivate
