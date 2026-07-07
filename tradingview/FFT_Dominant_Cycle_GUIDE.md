---
title: FFT Dominant Cycle — TradingView Indicator
type: indicator_guide
updated: 2026-05-07
---

# FFT Dominant Cycle — Guida TradingView

## Collegamento backtest
- [[../03_STRATEGIES/TESTED/11_FFT_Dominant_Cycle]] — risultati OOS 2021-2025
- File Pine Script: `tradingview/FFT_Dominant_Cycle_v1.pine`

## Come caricare su TradingView

1. Apri TradingView → Pine Script Editor (in basso)
2. Copia tutto il contenuto di `FFT_Dominant_Cycle_v1.pine`
3. Incolla nell'editor e clicca **Save** poi **Add to chart**
4. L'indicatore appare nel pannello inferiore

## Parametri — setup consigliato da backtest

| Parametro | Valore consigliato | Note |
|-----------|-------------------|------|
| FFT Window | **64** | N=64 in Pine (N=256 nel backtest Python — vedi nota) |
| Low Freq Cutoff | **0.10** | Esclude bin trend |
| High Freq Cutoff | **0.20** | Esclude bin rumore |
| Min Cycle Period | **10** barre | Filtro cicli troppo brevi |
| Min SNR | **1.5** | Quality gate |
| Session Filter | **London (07-16 UTC)** | Migliore su M15 da backtest |

## ⚠️ Nota su N=64 vs N=256

Il backtest Python usa N=256 su M15 (ottimale). Pine Script con N=256 diventerebbe
molto lento perché esegue `23 bins × 256 ops = 5888 calcoli per barra` in loop.

N=64 è il compromesso pratico per TradingView:
- Performance OK su chart normali
- Cattura cicli fino a 64/2 = 32 barre (8h su M15)
- Leggermente meno preciso dei cicli da 25-64 barre del backtest

Se il chart è lento: riduci N a 32.

## Lettura del pannello

```
  +1.0  ─────────────────────────────────────
  +0.5  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
   0.0  ─────────────────── ▲ ─────────────  ← segnale LONG (trough, ciclo risale)
  -0.5  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·  ·
  -1.0  ─────────────────────────────────────
        └── zona ribassista (fill rosso)
        └── ▽ = segnale SHORT (peak, ciclo scende)
```

- **Linea verde** = ciclo sopra zero (fase ascendente)
- **Linea rossa** = ciclo sotto zero (fase discendente)
- **▲ triangolo verde** = zero-crossing slope verso l'alto = LONG (trough)
- **▽ triangolo rosso** = zero-crossing slope verso il basso = SHORT (peak)
- **Cerchietti piccoli** = segnali sotto la soglia di qualità (usare con cautela)
- **Linea arancione** = periodo dominante scalato (quando cambia = ciclo diverso)
- **Sfondo colorato** = sessione attiva (blu=London, viola=NY, arancio=Asian)

## Come interpretare i segnali

### Segnale forte (triangolo pieno)
- SNR ≥ 1.5: il ciclo dominante ha almeno 1.5× la potenza media della banda
- Periodo ≥ 10 barre: il ciclo è abbastanza lungo da essere significativo
- Nella sessione selezionata

### Segnale debole (cerchio piccolo)
- Il ciclo c'è ma SNR o periodo non superano la soglia
- Può essere usato come conferma aggiuntiva ma non standalone

## Combinazione con altri segnali (per Pipeline Bot)

Il backtest ha dimostrato che il FFT Cycle standalone ha OOS PF=1.17 su M15.
Per avvicinarsi alla soglia target (PF > 1.3) si consiglia di usarlo in confluenza:

1. **FFT Cycle (questo indicatore)** → contesto: ciclo in fase long/short?
2. **Derivate (da implementare come #17)** → timing: la derivata del prezzo conferma?
3. **Fractal S/R** → geometria: il segnale è vicino a un livello S/R?

Entry solo quando tutti e tre concordano.

## Configurazioni per TF diversi

| TF | N | Min Period | Session | Note |
|----|---|-----------|---------|------|
| M15 | 64 | 10 | London | Setup principale backtest |
| M5  | 64 | 10 | London/NY | Più trade, più rumore |
| H1  | 32 | 5  | All Day | Cicli più lenti e chiari |
| H4  | 32 | 4  | All Day | Swing trading |

## Limitazioni

1. **Latenza**: la DFT vede la storia, non il futuro — il segnale è al primo bar dopo il trough/peak
2. **Non-stazionarietà**: il periodo dominante cambia nel tempo — normale, gestito dal rolling window
3. **N=64 in Pine vs N=256 nel backtest**: leggera differenza nei risultati attesi
4. **Slippage non conteggiato**: in live trading il risultato sarà inferiore al backtest
5. **Performance**: su chart con molte barre storiche il calcolo iniziale può essere lento

## Changelog
- v1 (2026-05-07): prima implementazione, consistente con backtest Python #11
