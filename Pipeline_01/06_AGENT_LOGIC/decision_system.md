# Decision Engine

## Collegamenti
- [[../00_CORE/Vision]]
- [[../01_THEORY/INDEX]]
- [[../03_STRATEGIES/INDEX]]
- [[../08_EXECUTION/INDEX]]
- [[../11_MEMORY/PROJECT_STATE]]

## Input
- FFT signal
- dP
- d2P
- pattern or geometry score
- time-price confluence score
- regime filter

## Logica
### Buy
- ciclo minimo o contesto favorevole
- confluenza geometrico-temporale favorevole
- `dP > 0`
- `d2P > 0`

### Sell
- ciclo massimo o contesto favorevole
- confluenza geometrico-temporale favorevole
- `dP < 0`
- `d2P < 0`

## Output
- segnale
- confidence score
- contesto operativo
- motivo della confluenza
