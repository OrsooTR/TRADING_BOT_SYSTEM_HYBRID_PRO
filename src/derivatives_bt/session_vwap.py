from __future__ import annotations

import math
from dataclasses import dataclass

import backtrader as bt
import pandas as pd

from derivatives_bt.backtest import PandasPriceData, RunConfig, TradeStatsAnalyzer


SESSION_SPECS: dict[str, tuple[int, int]] = {
    "day": (0, 24),
    "london": (7, 16),
    "newyork": (13, 21),
}


def add_session_vwap_features(frame: pd.DataFrame) -> pd.DataFrame:
    enriched = frame.copy()
    typical_price = (enriched["high"] + enriched["low"] + enriched["close"]) / 3.0
    volume = enriched["volume"].where(enriched["volume"] > 0.0, 1.0)
    # HistData usa timestamp EST (GMT-5, no DST): shift a UTC prima delle sessioni.
    # Il raggruppamento per session_day resta sulla data EST dell'indice: le sessioni
    # shiftate (london 2-11 EST, newyork 8-16 EST) non attraversano la mezzanotte EST,
    # quindi ogni sessione cade interamente in un solo giorno EST.
    hours = (enriched.index.hour + 5) % 24

    for session_label, (start_hour, end_hour) in SESSION_SPECS.items():
        active_mask = (hours >= start_hour) & (hours < end_hour)
        session_frame = enriched.loc[active_mask, ["open", "high", "low", "close", "volume"]].copy()
        session_frame["typical_price"] = typical_price.loc[active_mask]
        session_frame["volume_adj"] = volume.loc[active_mask]
        session_frame["session_day"] = pd.Index(session_frame.index.normalize(), name="session_day")

        turnover = session_frame["typical_price"] * session_frame["volume_adj"]
        cum_turnover = turnover.groupby(session_frame["session_day"]).cumsum()
        cum_volume = session_frame["volume_adj"].groupby(session_frame["session_day"]).cumsum()
        session_bar = session_frame.groupby("session_day").cumcount() + 1
        session_size = session_bar.groupby(session_frame["session_day"]).transform("max")
        session_close = (session_bar == session_size).astype(float)

        vwap = cum_turnover.div(cum_volume.where(cum_volume > 0.0))

        enriched[f"session_vwap_{session_label}"] = float("nan")
        enriched[f"session_bar_{session_label}"] = 0.0
        enriched[f"session_active_{session_label}"] = 0.0
        enriched[f"session_close_{session_label}"] = 0.0

        enriched.loc[active_mask, f"session_vwap_{session_label}"] = vwap.to_numpy()
        enriched.loc[active_mask, f"session_bar_{session_label}"] = session_bar.astype(float).to_numpy()
        enriched.loc[active_mask, f"session_active_{session_label}"] = 1.0
        enriched.loc[active_mask, f"session_close_{session_label}"] = session_close.to_numpy()

    return enriched


class SessionVwapData(PandasPriceData):
    lines = (
        "session_vwap_day",
        "session_bar_day",
        "session_active_day",
        "session_close_day",
        "session_vwap_london",
        "session_bar_london",
        "session_active_london",
        "session_close_london",
        "session_vwap_newyork",
        "session_bar_newyork",
        "session_active_newyork",
        "session_close_newyork",
    )
    params = tuple(PandasPriceData.params._gettuple()) + tuple((line, line) for line in lines)


class SessionVwapMeanReversionStrategy(bt.Strategy):
    params = (
        ("session_label", "day"),
        ("min_session_bars", 30),
        ("entry_atr_mult", 2.0),
        ("rejection_frac", 0.25),
        ("sl_atr_mult", 1.0),
        ("rr", 2.0),
        ("risk_per_trade", 0.01),
        ("leverage", 30.0),
        ("year_end_cutoff_day", 20),
    )

    def __init__(self) -> None:
        self.atr = bt.ind.ATR(self.data, period=14)
        self.entry_order: bt.Order | None = None
        self.stop_order: bt.Order | None = None
        self.target_order: bt.Order | None = None
        self.close_order: bt.Order | None = None
        self.pending_direction: str | None = None
        self.pending_stop_distance: float | None = None
        self.pending_target_price: float | None = None

        self.session_fields = {
            "day": {
                "vwap": self.data.session_vwap_day,
                "bar": self.data.session_bar_day,
                "active": self.data.session_active_day,
                "close": self.data.session_close_day,
            },
            "london": {
                "vwap": self.data.session_vwap_london,
                "bar": self.data.session_bar_london,
                "active": self.data.session_active_london,
                "close": self.data.session_close_london,
            },
            "newyork": {
                "vwap": self.data.session_vwap_newyork,
                "bar": self.data.session_bar_newyork,
                "active": self.data.session_active_newyork,
                "close": self.data.session_close_newyork,
            },
        }

    def _min_bars(self) -> int:
        return max(20, int(self.p.min_session_bars) + 2)

    def _has_pending_orders(self) -> bool:
        return any(
            order is not None
            for order in (self.entry_order, self.stop_order, self.target_order, self.close_order)
        )

    def _calc_size(self, stop_distance: float) -> int:
        account_value = float(self.broker.getvalue())
        cash_risk = account_value * float(self.p.risk_per_trade)
        risk_size = int(cash_risk / stop_distance) if stop_distance > 0 else 0

        current_price = float(self.data.close[0])
        max_size = int((account_value * float(self.p.leverage)) / current_price) if current_price > 0 else 0
        return max(0, min(risk_size, max_size))

    def _current_session_values(self, offset: int = 0) -> tuple[float | None, float, float, float]:
        session_state = self.session_fields[str(self.p.session_label)]
        vwap = float(session_state["vwap"][offset])
        bar_num = float(session_state["bar"][offset])
        active = float(session_state["active"][offset])
        is_close_bar = float(session_state["close"][offset])
        if math.isnan(vwap):
            return None, bar_num, active, is_close_bar
        return vwap, bar_num, active, is_close_bar

    def _is_year_end(self) -> bool:
        dt = self.data.datetime.datetime(0)
        return dt.month == 12 and dt.day >= int(self.p.year_end_cutoff_day)

    def _cancel_exit_orders(self) -> None:
        for order in (self.stop_order, self.target_order):
            if order is not None:
                self.cancel(order)

    def _submit_entry(self, direction: str, stop_distance: float, target_price: float) -> None:
        size = self._calc_size(stop_distance)
        if size <= 0:
            return

        self.pending_direction = direction
        self.pending_stop_distance = stop_distance
        self.pending_target_price = target_price
        if direction == "long":
            self.entry_order = self.buy(size=size)
        else:
            self.entry_order = self.sell(size=size)

    def next(self) -> None:
        if len(self) < self._min_bars():
            return

        current_vwap, session_bar, session_active, session_close = self._current_session_values(0)
        previous_vwap, _, previous_active, _ = self._current_session_values(-1)
        atr_now = float(self.atr[0])
        atr_prev = float(self.atr[-1])

        if self.position:
            if session_close >= 0.5 and self.close_order is None:
                self._cancel_exit_orders()
                self.close_order = self.close()
            return

        if self._has_pending_orders():
            return

        if (
            current_vwap is None
            or previous_vwap is None
            or math.isnan(atr_now)
            or math.isnan(atr_prev)
            or atr_now <= 0
            or atr_prev <= 0
            or session_active < 0.5
            or previous_active < 0.5
            or session_close >= 0.5
            or session_bar < float(self.p.min_session_bars)
            or self._is_year_end()
        ):
            return

        close_now = float(self.data.close[0])
        close_prev = float(self.data.close[-1])
        stop_distance = atr_now * float(self.p.sl_atr_mult)
        room_to_vwap = abs(current_vwap - close_now)
        min_room = stop_distance * 2.0
        if room_to_vwap < min_room:
            return

        prev_band = atr_prev * float(self.p.entry_atr_mult)
        band_now = atr_now * float(self.p.entry_atr_mult)
        candle_range = max(float(self.data.high[0]) - float(self.data.low[0]), 1e-8)
        bullish_rejection = (close_now - float(self.data.low[0])) / candle_range >= float(self.p.rejection_frac)
        bearish_rejection = (float(self.data.high[0]) - close_now) / candle_range >= float(self.p.rejection_frac)

        long_signal = (
            close_prev >= previous_vwap - prev_band
            and close_now <= current_vwap - band_now
            and close_now < current_vwap
            and bullish_rejection
        )
        short_signal = (
            close_prev <= previous_vwap + prev_band
            and close_now >= current_vwap + band_now
            and close_now > current_vwap
            and bearish_rejection
        )

        if long_signal:
            target_price = close_now + min(stop_distance * float(self.p.rr), current_vwap - close_now)
            if target_price > close_now:
                self._submit_entry("long", stop_distance, target_price)
        elif short_signal:
            target_price = close_now - min(stop_distance * float(self.p.rr), close_now - current_vwap)
            if target_price < close_now:
                self._submit_entry("short", stop_distance, target_price)

    def notify_order(self, order: bt.Order) -> None:
        if order.status in (bt.Order.Submitted, bt.Order.Accepted):
            return

        if order == self.entry_order:
            if order.status == bt.Order.Completed:
                stop_distance = float(self.pending_stop_distance or 0.0)
                target_price = float(self.pending_target_price or order.executed.price)
                if stop_distance > 0 and self.position.size > 0:
                    stop_price = order.executed.price - stop_distance
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
                elif stop_distance > 0 and self.position.size < 0:
                    size = abs(self.position.size)
                    stop_price = order.executed.price + stop_distance
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
                    self.pending_stop_distance = None
                    self.pending_target_price = None
            return

        if order == self.close_order:
            if order.status in (bt.Order.Completed, bt.Order.Canceled, bt.Order.Margin, bt.Order.Rejected):
                self.close_order = None
                if not self.position:
                    self.pending_direction = None
                    self.pending_stop_distance = None
                    self.pending_target_price = None
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
                self.pending_stop_distance = None
                self.pending_target_price = None


VWAP_PARAM_COLS = [
    "session_label",
    "min_session_bars",
    "entry_atr_mult",
    "rejection_frac",
    "sl_atr_mult",
    "rr",
]


def make_vwap_feed(frame: pd.DataFrame) -> SessionVwapData:
    return SessionVwapData(dataname=frame.copy())


def run_vwap_optimization(
    frame: pd.DataFrame,
    parameter_grid: dict[str, list[str | float | int]],
    config: RunConfig,
    maxcpus: int | None = None,
) -> list[dict[str, str | float | int]]:
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
    cerebro.adddata(make_vwap_feed(frame))
    cerebro.addanalyzer(TradeStatsAnalyzer, _name="trade_stats")
    cerebro.optstrategy(
        SessionVwapMeanReversionStrategy,
        session_label=parameter_grid["session_label"],
        min_session_bars=parameter_grid["min_session_bars"],
        entry_atr_mult=parameter_grid["entry_atr_mult"],
        rejection_frac=parameter_grid["rejection_frac"],
        sl_atr_mult=parameter_grid["sl_atr_mult"],
        rr=parameter_grid["rr"],
        risk_per_trade=config.risk_per_trade,
        leverage=config.leverage,
    )

    raw_results = cerebro.run()
    collected: list[dict[str, str | float | int]] = []

    for result in raw_results:
        strat = result[0]
        metrics = strat.analyzers.trade_stats.get_analysis()
        params = dict(strat.params._getkwargs())
        collected.append(
            {
                "session_label": str(params["session_label"]),
                "min_session_bars": int(params["min_session_bars"]),
                "entry_atr_mult": float(params["entry_atr_mult"]),
                "rejection_frac": float(params["rejection_frac"]),
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
        )

    return collected


__all__ = [
    "SESSION_SPECS",
    "RunConfig",
    "VWAP_PARAM_COLS",
    "add_session_vwap_features",
    "run_vwap_optimization",
]
