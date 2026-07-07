# Backtest VWAP Session Mean Reversion EURUSD ALL_TFS

## Related Notes
- [[../../../Pipeline_01/04_BACKTEST/INDEX]]
- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]
- [[../../../Pipeline_01/09_LOGS/esperimenti]]
- [[../../../Pipeline_01/11_MEMORY/PROJECT_STATE]]

- Generated: 2026-04-28 09:45:57 UTC
- Mode: smoke
- Combinations: 4
- Ranking: OOS Profit Factor desc, OOS Max DD asc, OOS P&L desc

## Logic
- Trigger long: close extends below session VWAP by ATR band and the candle rejects the lows.
- Trigger short: close extends above session VWAP by ATR band and the candle rejects the highs.
- Stop: ATR x sl_atr_mult
- Target: min(session VWAP room, stop x RR), with minimum room >= 2R

## Best Setup
- TF: M1
- Session: day
- Min Session Bars: 30
- Entry ATR Mult: 1.50
- Rejection Fraction: 0.25
- SL ATR: 1.00
- RR Cap: 3.0
- Train PF: 1.010
- OOS PF: 1.865
- OOS DD %: 15.33
- OOS P&L %: 58.95

## Top 10

| Rank | TF | Session | Bars | Entry ATR | Reject | SL ATR | RR | Train PF | OOS PF | OOS DD % | OOS P&L % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | M1 | day | 30 | 1.50 | 0.25 | 1.00 | 3.0 | 1.010 | 1.865 | 15.33 | 58.95 |
| 2 | M1 | day | 30 | 1.50 | 0.25 | 1.00 | 2.0 | 1.003 | 1.846 | 16.20 | 57.26 |
| 3 | M1 | day | 30 | 2.00 | 0.25 | 1.00 | 3.0 | 0.815 | 1.204 | 41.09 | 60.36 |
| 4 | M1 | day | 30 | 2.00 | 0.25 | 1.00 | 2.0 | 0.809 | 1.204 | 41.09 | 60.21 |
