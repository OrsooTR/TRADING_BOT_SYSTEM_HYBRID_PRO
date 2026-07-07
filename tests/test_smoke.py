"""Smoke test del motore di backtest vettoriale.

Verifica su dati sintetici le proprietà chiave del simulatore:
- tie-break pessimistico (TP e SL nella stessa barra = perdita)
- costo spread sottratto da ogni trade
- chiusura mark-to-market dei trade in timeout

Eseguibile senza pytest: `python tests/test_smoke.py`
"""

import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_sim_and_metrics():
    atr = load_module("run_atr_vectorized", ROOT / "scripts" / "run_atr_vectorized.py")

    N = 30
    high = np.full(N, 1.0)
    low = np.full(N, 1.0)
    close = np.full(N, 1.0)

    # Trade A: long da barra 2, TP (1.02) colpito alla barra 5
    high[5] = 1.03
    # Trade B: long da barra 10, TP e SL nella STESSA barra 12 -> deve perdere
    high[12] = 1.03
    low[12] = 0.985
    # Trade C: long da barra 20, nessun hit entro max_hold=5 -> mark-to-market
    close[24] = 1.005

    entry_bars = np.array([2, 10, 20])
    directions = np.array([1.0, 1.0, 1.0])
    ep = np.array([1.0, 1.0, 1.0])
    sl_d = np.array([0.01, 0.01, 0.01])

    m = atr.sim_and_metrics(entry_bars, directions, ep, sl_d, rr=2.0,
                            high=high, low=low, close=close, max_hold=5)

    assert m["trades"] == 3, m
    # solo il trade A vince: tie-break pessimistico su B
    assert abs(m["win_rate"] - 33.33) < 0.1, m
    # PF atteso: spread_R = SPREAD/0.01; gp = (2-s) + (0.5-s); gl = 1+s
    s = atr.SPREAD / 0.01
    exp_pf = ((2 - s) + (0.5 - s)) / (1 + s)
    assert abs(m["profit_factor"] - exp_pf) < 0.01, (m["profit_factor"], exp_pf)
    print(f"OK sim_and_metrics: win_rate={m['win_rate']}  PF={m['profit_factor']} (atteso {exp_pf:.4f})")


def test_smask_est_shift():
    atr = load_module("run_atr_vectorized", ROOT / "scripts" / "run_atr_vectorized.py")
    import pandas as pd
    # 08:00 EST = 13:00 UTC -> dentro sessione newyork (13-21 UTC)
    idx = pd.DatetimeIndex(["2024-01-02 08:00:00"])
    assert atr.smask(idx, "newyork").tolist() == [True]
    # 08:00 EST = 13:00 UTC -> dentro anche london (7-16 UTC)
    assert atr.smask(idx, "london").tolist() == [True]
    # 20:00 EST = 01:00 UTC -> asian (0-8 UTC)
    idx2 = pd.DatetimeIndex(["2024-01-02 20:00:00"])
    assert atr.smask(idx2, "asian").tolist() == [True]
    assert atr.smask(idx2, "london").tolist() == [False]
    print("OK smask: shift EST->UTC corretto")


def test_stats_generator():
    gen = load_module("generate_dashboard_stats", ROOT / "scripts" / "generate_dashboard_stats.py")
    backlog = gen.parse_backlog()
    assert backlog, "backlog vuoto"
    state = gen.parse_project_state()
    assert state["strategies"], "strategie non trovate in PROJECT_STATE"
    print(f"OK stats generator: {len(backlog)} item backlog, {len(state['strategies'])} strategie")


if __name__ == "__main__":
    test_sim_and_metrics()
    test_smask_est_shift()
    test_stats_generator()
    print("SMOKE TEST OK")
    sys.exit(0)
