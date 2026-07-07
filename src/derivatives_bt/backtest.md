# Code Doc - backtest.py

## Source
- `src/derivatives_bt/backtest.py`
- [Apri il file Python sorgente](backtest.py)
- [Torna all indice del codice](../../Pipeline_01/12_CODE/INDEX.md)

## Scopo
Motore principale dei backtest a derivate con strategia Backtrader, sizing, gestione ordini e metriche finali.

## Punti Chiave
- Definisce la strategia `DerivativeCrossStrategy` basata su EMA, derivata prima e derivata seconda.
- Implementa il sizing in funzione del rischio per trade, ATR e leva massima.
- Produce metriche aggregate come PF, win rate, drawdown e distribuzione long/short.
- Espone `run_optimization()` per lanciare grid search su insiemi di parametri.

## Collegamenti
- [02_Derivative_1st_2nd_Order](../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order.md)
- [INDEX](../../Pipeline_01/04_BACKTEST/DERIVATIVE_tests/INDEX.md)
- [decision_system](../../Pipeline_01/06_AGENT_LOGIC/decision_system.md)

## Codice Completo
```python
from __future__ import annotations

import math
from dataclasses import dataclass

import backtrader as bt
import pandas as pd


@dataclass(frozen=True)
class RunConfig:
    initial_cash: float = 100_000.0
    risk_per_trade: float = 0.01
    leverage: float = 30.0
    slippage_per_side: float = 0.00005


class PandasPriceData(bt.feeds.PandasData):
    params = (
        ("datetime", None),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("openinterest", -1),
    )


class TradeStatsAnalyzer(bt.Analyzer):
    def start(self) -> None:
        self.initial_value = float(self.strategy.broker.getvalue())
        self.closed_equity = self.initial_value
        self.peak_value = self.initial_value
        self.max_drawdown_pct = 0.0
        self.gross_profit = 0.0
        self.gross_loss = 0.0
        self.total_trades = 0
        self.wins = 0
        self.longs = 0
        self.shorts = 0
        self.total_bars = 0
        self.rets: dict[str, float] = {}

    def notify_trade(self, trade: bt.Trade) -> None:
        if not trade.isclosed:
            return

        pnl = float(trade.pnlcomm)
        self.total_trades += 1
        self.total_bars += max(int(trade.barlen), 0)

        if trade.long:
            self.longs += 1
        else:
            self.shorts += 1

        if pnl > 0:
            self.gross_profit += pnl
            self.wins += 1
        elif pnl < 0:
            self.gross_loss += pnl

        self.closed_equity += pnl
        if self.closed_equity > self.peak_value:
            self.peak_value = self.closed_equity

        if self.peak_value > 0:
            drawdown_pct = (self.peak_value - self.closed_equity) / self.peak_value * 100.0
            self.max_drawdown_pct = max(self.max_drawdown_pct, drawdown_pct)

    def stop(self) -> None:
        losses_abs = abs(self.gross_loss)

        if losses_abs > 0:
            profit_factor = self.gross_profit / losses_abs
        elif self.gross_profit > 0:
            profit_factor = float("inf")
        else:
            profit_factor = 0.0

        self.rets = {
            "trades": int(self.total_trades),
            "win_rate": (self.wins / self.total_trades * 100.0) if self.total_trades else 0.0,
            "profit_factor": profit_factor,
            "max_drawdown_pct": self.max_drawdown_pct,
            "pnl_pct": (self.closed_equity / self.initial_value - 1.0) * 100.0,
            "longs": int(self.longs),
            "shorts": int(self.shorts),
            "avg_bars": (self.total_bars / self.total_trades) if self.total_trades else 0.0,
            "gross_profit": self.gross_profit,
            "gross_loss": self.gross_loss,
        }

    def get_analysis(self) -> dict[str, float]:
        return self.rets


class DerivativeCrossStrategy(bt.Strategy):
    params = (
        ("smooth_period", 5),
        ("d1_period", 2),
        ("d2_period", 2),
        ("d1_threshold", 0.05),
        ("d2_threshold", 0.0),
        ("sl_atr_mult", 1.0),
        ("rr", 2.0),
        ("risk_per_trade", 0.01),
        ("leverage", 30.0),
    )

    def __init__(self) -> None:
        self.ema = bt.ind.EMA(self.data.close, period=self.p.smooth_period)
        self.atr = bt.ind.ATR(self.data, period=14)
        self.entry_order: bt.Order | None = None
        self.stop_order: bt.Order | None = None
        self.target_order: bt.Order | None = None
        self.pending_direction: str | None = None

    def _min_bars(self) -> int:
        return max(self.p.smooth_period, 14) + self.p.d1_period + self.p.d2_period + 2

    def _calc_d1(self, offset: int) -> float | None:
        atr_value = float(self.atr[offset])
        if math.isnan(atr_value) or atr_value <= 0:
            return None
        return (float(self.ema[offset]) - float(self.ema[offset - self.p.d1_period])) / atr_value

    def _calc_d2(self, offset: int) -> float | None:
        d1_now = self._calc_d1(offset)
        d1_prev = self._calc_d1(offset - self.p.d2_period)
        if d1_now is None or d1_prev is None:
            return None
        return d1_now - d1_prev

    def _has_pending_orders(self) -> bool:
        return any(order is not None for order in (self.entry_order, self.stop_order, self.target_order))

    def _calc_size(self, stop_distance: float) -> int:
        account_value = float(self.broker.getvalue())
        cash_risk = account_value * float(self.p.risk_per_trade)
        risk_size = int(cash_risk / stop_distance) if stop_distance > 0 else 0

        current_price = float(self.data.close[0])
        max_size = int((account_value * float(self.p.leverage)) / current_price) if current_price > 0 else 0
        return max(0, min(risk_size, max_size))

    def _submit_entry(self, direction: str) -> None:
        atr_value = float(self.atr[0])
        if math.isnan(atr_value) or atr_value <= 0:
            return

        stop_distance = atr_value * float(self.p.sl_atr_mult)
        size = self._calc_size(stop_distance)
        if size <= 0:
            return

        self.pending_direction = direction
        if direction == "long":
            self.entry_order = self.buy(size=size)
        else:
            self.entry_order = self.sell(size=size)

    def next(self) -> None:
        if len(self) < self._min_bars():
            return

        if self.position or self._has_pending_orders():
            return

        d1_now = self._calc_d1(0)
        d1_prev = self._calc_d1(-1)
        d2_now = self._calc_d2(0)

        if d1_now is None or d1_prev is None or d2_now is None:
            return

        long_cross = d1_prev <= self.p.d1_threshold and d1_now > self.p.d1_threshold
        short_cross = d1_prev >= -self.p.d1_threshold and d1_now < -self.p.d1_threshold

        if long_cross and d2_now > self.p.d2_threshold:
            self._submit_entry("long")
        elif short_cross and d2_now < -self.p.d2_threshold:
            self._submit_entry("short")

    def notify_order(self, order: bt.Order) -> None:
        if order.status in (bt.Order.Submitted, bt.Order.Accepted):
            return

        if order == self.entry_order:
            if order.status == bt.Order.Completed:
                atr_value = float(self.atr[0])
                stop_distance = atr_value * float(self.p.sl_atr_mult)
                if self.position.size > 0:
                    stop_price = order.executed.price - stop_distance
                    target_price = order.executed.price + stop_distance * float(self.p.rr)
                    self.stop_order = self.sell(
                        size=self.position.size,
                        exectype=bt.Order.Stop,
                        price=stop_price,
                    )
                    self.target_order = self.sell(
                        size=self.position.size,
                        exectype=bt.Order.Limit,
                        price=target_price,
                        oco=self.stop_order,
                    )
                elif self.position.size < 0:
                    size = abs(self.position.size)
                    stop_price = order.executed.price + stop_distance
                    target_price = order.executed.price - stop_distance * float(self.p.rr)
                    self.stop_order = self.buy(
                        size=size,
                        exectype=bt.Order.Stop,
                        price=stop_price,
                    )
                    self.target_order = self.buy(
                        size=size,
                        exectype=bt.Order.Limit,
                        price=target_price,
                        oco=self.stop_order,
                    )

            if order.status in (bt.Order.Completed, bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected):
                self.entry_order = None
                if order.status != bt.Order.Completed:
                    self.pending_direction = None
            return

        if order in (self.stop_order, self.target_order):
            if order == self.stop_order and order.status in (
                bt.Order.Completed,
                bt.Order.Canceled,
                bt.Order.Margin,
                bt.Order.Rejected,
            ):
                self.stop_order = None
            if order == self.target_order and order.status in (
                bt.Order.Completed,
                bt.Order.Canceled,
                bt.Order.Margin,
                bt.Order.Rejected,
            ):
                self.target_order = None

            if not self.position and self.stop_order is None and self.target_order is None:
                self.pending_direction = None


def make_data_feed(frame: pd.DataFrame) -> PandasPriceData:
    return PandasPriceData(dataname=frame.copy())


def run_optimization(
    frame: pd.DataFrame,
    parameter_grid: dict[str, list[float | int]],
    config: RunConfig,
    maxcpus: int | None = None,
) -> list[dict[str, float | int]]:
    cerebro = bt.Cerebro(optreturn=True, maxcpus=maxcpus, stdstats=False)
    cerebro.broker.setcash(config.initial_cash)
    cerebro.broker.setcommission(commission=0.0, leverage=config.leverage)
    cerebro.broker.set_slippage_fixed(
        fixed=config.slippage_per_side,
        slip_open=True,
        slip_limit=True,
        slip_match=True,
        slip_out=False,
    )
    cerebro.adddata(make_data_feed(frame))
    cerebro.addanalyzer(TradeStatsAnalyzer, _name="trade_stats")
    cerebro.optstrategy(
        DerivativeCrossStrategy,
        smooth_period=parameter_grid["smooth_period"],
        d1_period=parameter_grid["d1_period"],
        d2_period=parameter_grid["d2_period"],
        d1_threshold=parameter_grid["d1_threshold"],
        d2_threshold=parameter_grid["d2_threshold"],
        sl_atr_mult=parameter_grid["sl_atr_mult"],
        rr=parameter_grid["rr"],
        risk_per_trade=config.risk_per_trade,
        leverage=config.leverage,
    )

    raw_results = cerebro.run()
    collected: list[dict[str, float | int]] = []

    for result in raw_results:
        strat = result[0]
        metrics = strat.analyzers.trade_stats.get_analysis()
        params = dict(strat.params._getkwargs())
        metrics_row = {
            "smooth_period": int(params["smooth_period"]),
            "d1_period": int(params["d1_period"]),
            "d2_period": int(params["d2_period"]),
            "d1_threshold": float(params["d1_threshold"]),
            "d2_threshold": float(params["d2_threshold"]),
            "sl_atr_mult": float(params["sl_atr_mult"]),
            "rr": float(params["rr"]),
            "trades": int(metrics["trades"]),
            "win_rate": float(metrics["win_rate"]),
            "profit_factor": float(metrics["profit_factor"]),
            "max_drawdown_pct": float(metrics["max_drawdown_pct"]),
            "pnl_pct": float(metrics["pnl_pct"]),
            "longs": int(metrics["longs"]),
            "shorts": int(metrics["shorts"]),
            "avg_bars": float(metrics["avg_bars"]),
        }
        collected.append(metrics_row)

    return collected
```
