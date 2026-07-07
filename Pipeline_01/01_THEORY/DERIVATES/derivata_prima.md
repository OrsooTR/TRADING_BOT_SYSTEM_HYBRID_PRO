# Derivata Prima e Seconda

## Collegamenti
- [[../INDEX]]
- [[../../06_AGENT_LOGIC/decision_system]]
- [[../../03_STRATEGIES/IDEAS/fft_trend_following]]
- [[../../03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order]]

## Derivata Prima
`dP = P(t) - P(t-1)`

### Uso
- direzione
- momentum base
- conferma del verso del segnale

### Regola base
- `dP > 0` -> bias bullish
- `dP < 0` -> bias bearish

## Derivata Seconda
`d2P = dP(t) - dP(t-1)`

### Uso
- accelerazione
- rallentamento
- possibili inversioni

### Insight
- cambio di segno -> possibile reversal
- `dP` e `d2P` insieme sono la base della strategia derivativa pre-FFT
