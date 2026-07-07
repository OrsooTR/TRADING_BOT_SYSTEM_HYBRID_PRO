from AlgorithmImports import *
import math
from datetime import datetime, timedelta

import numpy as np


class FftClockTriggerHftFilterM15(QCAlgorithm):
    def initialize(self):
        self.set_start_date(2020, 1, 1)
        self.set_end_date(2025, 12, 31)
        self.set_cash(100000)
        self._symbol = self.add_forex("EURUSD", Resolution.MINUTE, Market.OANDA).symbol
        self.set_warm_up(250, Resolution.MINUTE)

        self.train_end = datetime(2023, 12, 31, 23, 59)
        self.initial_cash = 100000.0
        self.risk_per_trade = 0.01
        self.leverage = 30.0
        self.slippage = 0.00005

        self.close_window = []
        self.max_fft_window = 192
        self.prev_bar = None

        derivative_grid = {
            "smooth_period": [10, 20],
            "d1_period": [2, 4],
            "d2_period": [2],
            "d1_threshold": [0.05, 0.10],
            "d2_threshold": [0.00],
            "sl_atr_mult": [1.5],
            "rr": [2.0, 3.0],
        }
        filter_grid = {
            "fft_spec": [(96, 4), (96, 16), (192, 96)],
            "strength_threshold": [1.5, 2.5],
            "filter_action": ["avoid", "reduce"],
        }

        self.strategies = []
        idx = 0
        for smooth_period in derivative_grid["smooth_period"]:
            for d1_period in derivative_grid["d1_period"]:
                for d2_period in derivative_grid["d2_period"]:
                    for d1_threshold in derivative_grid["d1_threshold"]:
                        for d2_threshold in derivative_grid["d2_threshold"]:
                            for sl_atr_mult in derivative_grid["sl_atr_mult"]:
                                for rr in derivative_grid["rr"]:
                                    for fft_spec in filter_grid["fft_spec"]:
                                        for strength_threshold in filter_grid["strength_threshold"]:
                                            for filter_action in filter_grid["filter_action"]:
                                                params = {
                                                    "smooth_period": smooth_period,
                                                    "d1_period": d1_period,
                                                    "d2_period": d2_period,
                                                    "d1_threshold": d1_threshold,
                                                    "d2_threshold": d2_threshold,
                                                    "sl_atr_mult": sl_atr_mult,
                                                    "rr": rr,
                                                    "fft_spec": fft_spec,
                                                    "strength_threshold": strength_threshold,
                                                    "filter_action": filter_action,
                                                }
                                                self.strategies.append(self._new_state(idx, params))
                                                idx += 1

        self.consolidate(self._symbol, timedelta(minutes=15), self.on_m15_bar)
        self.debug("FFT Clock Trigger HFT Filter M15 grid initialized: %d combinations" % len(self.strategies))

    def _new_state(self, idx, params):
        return {
            "id": idx,
            "params": params,
            "ema": None,
            "atr": None,
            "tr_values": [],
            "d1_values": [],
            "fft_hits": [],
            "position": 0,
            "entry": 0.0,
            "stop": 0.0,
            "target": 0.0,
            "size": 0,
            "train": self._new_metrics(),
            "oos": self._new_metrics(),
        }

    def _new_metrics(self):
        return {
            "equity": self.initial_cash,
            "closed_equity": self.initial_cash,
            "peak": self.initial_cash,
            "gross_profit": 0.0,
            "gross_loss": 0.0,
            "trades": 0,
            "wins": 0,
            "max_dd": 0.0,
        }

    def on_m15_bar(self, bar):
        if self.is_warming_up:
            return
        self.close_window.append(float(bar.Close))
        if len(self.close_window) > self.max_fft_window:
            self.close_window.pop(0)

        for state in self.strategies:
            self._update_strategy(state, bar)
        self.prev_bar = bar

    def _update_strategy(self, state, bar):
        p = state["params"]
        high = float(bar.High)
        low = float(bar.Low)
        close = float(bar.Close)

        if self.prev_bar is None:
            return

        prev_close = float(self.prev_bar.Close)
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        state["tr_values"].append(tr)
        if len(state["tr_values"]) > 14:
            state["tr_values"].pop(0)
        if len(state["tr_values"]) < 14:
            return

        if state["atr"] is None:
            state["atr"] = sum(state["tr_values"]) / 14.0
        else:
            state["atr"] = (state["atr"] * 13.0 + tr) / 14.0
        atr = state["atr"]
        if atr <= 0:
            return

        alpha = 2.0 / (float(p["smooth_period"]) + 1.0)
        if state["ema"] is None:
            state["ema"] = close
        else:
            state["ema"] = alpha * close + (1.0 - alpha) * state["ema"]

        state.setdefault("ema_history", []).append(state["ema"])
        if len(state["ema_history"]) > 50:
            state["ema_history"].pop(0)
        if len(state["ema_history"]) <= p["d1_period"] + p["d2_period"]:
            return

        d1 = (state["ema_history"][-1] - state["ema_history"][-1 - p["d1_period"]]) / atr
        state["d1_values"].append(d1)
        if len(state["d1_values"]) > 50:
            state["d1_values"].pop(0)
        if len(state["d1_values"]) <= p["d2_period"] + 1:
            return

        d1_prev = state["d1_values"][-2]
        d2 = d1 - state["d1_values"][-1 - p["d2_period"]]

        self._check_exit(state, bar)
        if state["position"] != 0:
            return

        clock_driven = self._clock_driven(state)
        if clock_driven and p["filter_action"] == "avoid":
            return

        risk_mult = 0.5 if clock_driven and p["filter_action"] == "reduce" else 1.0
        long_cross = d1_prev <= p["d1_threshold"] and d1 > p["d1_threshold"]
        short_cross = d1_prev >= -p["d1_threshold"] and d1 < -p["d1_threshold"]

        if long_cross and d2 > p["d2_threshold"]:
            self._open_position(state, 1, close, atr, risk_mult)
        elif short_cross and d2 < -p["d2_threshold"]:
            self._open_position(state, -1, close, atr, risk_mult)

    def _fft_strength(self, window, period):
        values = np.array(window, dtype=float)
        returns = np.diff(np.log(values))
        if len(returns) < 8:
            return None
        returns = returns - np.mean(returns)
        spectrum = np.abs(np.fft.rfft(returns))
        if len(spectrum) < 5:
            return None
        target_bin = int(round(len(returns) / float(period)))
        target_bin = max(1, min(target_bin, len(spectrum) - 1))
        low = max(1, target_bin - 3)
        high = min(len(spectrum), target_bin + 4)
        neighbors = np.delete(spectrum[low:high], target_bin - low)
        baseline = float(np.mean(neighbors)) if len(neighbors) else float(np.mean(spectrum[1:]))
        if baseline <= 0:
            return None
        return float(spectrum[target_bin] / baseline)

    def _clock_driven(self, state):
        window, period = state["params"]["fft_spec"]
        if len(self.close_window) < window:
            return False
        strength = self._fft_strength(self.close_window[-window:], period)
        if strength is None:
            return False
        hit = 1 if strength >= state["params"]["strength_threshold"] else 0
        state["fft_hits"].append(hit)
        if len(state["fft_hits"]) > 8:
            state["fft_hits"].pop(0)
        return len(state["fft_hits"]) >= 8 and sum(state["fft_hits"]) / float(len(state["fft_hits"])) >= 0.5

    def _open_position(self, state, direction, close, atr, risk_mult):
        stop_distance = atr * float(state["params"]["sl_atr_mult"])
        cash_risk = self.initial_cash * self.risk_per_trade * risk_mult
        size = int(cash_risk / stop_distance) if stop_distance > 0 else 0
        max_size = int((self.initial_cash * self.leverage) / close) if close > 0 else 0
        size = max(0, min(size, max_size))
        if size <= 0:
            return
        entry = close + self.slippage * direction
        state["position"] = direction
        state["entry"] = entry
        state["size"] = size
        if direction > 0:
            state["stop"] = entry - stop_distance
            state["target"] = entry + stop_distance * float(state["params"]["rr"])
        else:
            state["stop"] = entry + stop_distance
            state["target"] = entry - stop_distance * float(state["params"]["rr"])

    def _check_exit(self, state, bar):
        if state["position"] == 0:
            return
        direction = state["position"]
        high = float(bar.High)
        low = float(bar.Low)
        exit_price = None
        if direction > 0:
            if low <= state["stop"]:
                exit_price = state["stop"]
            elif high >= state["target"]:
                exit_price = state["target"]
        else:
            if high >= state["stop"]:
                exit_price = state["stop"]
            elif low <= state["target"]:
                exit_price = state["target"]
        if exit_price is None:
            return
        pnl = (exit_price - state["entry"]) * direction * state["size"]
        pnl -= self.slippage * state["size"]
        metrics = state["train"] if self.Time <= self.train_end else state["oos"]
        self._record_trade(metrics, pnl)
        state["position"] = 0
        state["size"] = 0

    def _record_trade(self, m, pnl):
        m["trades"] += 1
        if pnl > 0:
            m["wins"] += 1
            m["gross_profit"] += pnl
        elif pnl < 0:
            m["gross_loss"] += pnl
        m["closed_equity"] += pnl
        if m["closed_equity"] > m["peak"]:
            m["peak"] = m["closed_equity"]
        if m["peak"] > 0:
            m["max_dd"] = max(m["max_dd"], (m["peak"] - m["closed_equity"]) / m["peak"] * 100.0)

    def _pf(self, m):
        loss = abs(m["gross_loss"])
        if loss > 0:
            return m["gross_profit"] / loss
        return 999.0 if m["gross_profit"] > 0 else 0.0

    def _pnl_pct(self, m):
        return (m["closed_equity"] / self.initial_cash - 1.0) * 100.0

    def _wr(self, m):
        return (m["wins"] / float(m["trades"]) * 100.0) if m["trades"] else 0.0

    def on_end_of_algorithm(self):
        ranked = sorted(
            self.strategies,
            key=lambda s: (self._pf(s["oos"]), -s["oos"]["max_dd"], self._pnl_pct(s["oos"])),
            reverse=True,
        )
        self.debug("TOP 15 FFT Clock Trigger HFT Filter M15")
        for rank, state in enumerate(ranked[:15], start=1):
            p = state["params"]
            train = state["train"]
            oos = state["oos"]
            self.debug(
                "%02d fft=%s action=%s thr=%.2f smooth=%s d1=%s d1thr=%.2f sl=%.1f rr=%.1f | "
                "train PF=%.3f DD=%.2f pnl=%.2f trades=%d | "
                "OOS PF=%.3f DD=%.2f pnl=%.2f WR=%.1f trades=%d"
                % (
                    rank,
                    str(p["fft_spec"]),
                    p["filter_action"],
                    p["strength_threshold"],
                    p["smooth_period"],
                    p["d1_period"],
                    p["d1_threshold"],
                    p["sl_atr_mult"],
                    p["rr"],
                    self._pf(train),
                    train["max_dd"],
                    self._pnl_pct(train),
                    train["trades"],
                    self._pf(oos),
                    oos["max_dd"],
                    self._pnl_pct(oos),
                    self._wr(oos),
                    oos["trades"],
                )
            )
