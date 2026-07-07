# Strategia Idea - FFT Trend Following

## Collegamenti
- [[../INDEX]]
- [[../../01_THEORY/FFT/teoria_base]]
- [[../../01_THEORY/FFT/applicazione_trading]]
- [[../../01_THEORY/DERIVATES/derivata_prima]]
- [[../../06_AGENT_LOGIC/decision_system]]

## Idea
Usare FFT per filtrare il rumore e la derivata per la direzione.

## Logica
- segnale FFT pulito
- `dP > 0` -> long
- `dP < 0` -> short

## Parametri
- cutoff frequenze
- finestra FFT

## Rischi
- lag
- falsi segnali
- overfitting del filtro
