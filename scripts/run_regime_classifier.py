"""
FFT Spectral Regime Classifier (#12) — Vectorized Backtest
EURUSD M1/M5/M15 | Train: 2020 | OOS: 2021-2025

Regime è basato sulla DISTRIBUZIONE dell'energia spettrale dei log-return:
  - CYCLE : mid_ratio > hf_ratio + delta  (banda media strutturata)
  - NOISE : hf_ratio > mid_ratio + delta  (alta frequenza domina = casuale)
  - TREND : spectral_slope < slope_thresh (processo persistente)
  - TRANS : nessun dominante chiaro

Tre test:
  A) Forward return stats per regime (validation del classificatore)
  B) Derivate (#02) con e senza filtro regime
  C) RSI (#03) con e senza filtro regime

Ipotesi testate:
  - Derivate in CYCLE regime migliorano?
  - RSI in NOISE regime migliora? (mean-reversion in assenza di struttura)
  - Derivate in TREND regime (pendenza ripida) migliorano?
"""
from __future__ import annotations
import numpy as np, pandas as pd, os, time, json
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parent.parent
HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", ROOT / "data" / "histdata"))
ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
        for y in [2020,2021,2022,2023,2024,2025]]
OUT_DIR = ROOT / "artifacts" / "regime_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "regime_backtests" / "reports"

# ── Grid ─────────────────────────────────────────────────────────────────────
FFT_NS       = {"M1":[64], "M5":[64,128], "M15":[64,128]}
BAND_LO_PCT  = 0.10    # fisso: bins 1-10% = bassa freq
BAND_HI_PCT  = 0.60    # fisso: bins 60-100% = alta freq (banda media = 10-60%)
DELTAS       = [0.03, 0.05, 0.08]   # soglia |mid-hf| per CYCLE/NOISE
SLOPE_THRESH = [-1.0, -1.5]          # pendenza spettrale per TREND
SESSIONS     = ["all", "london", "newyork", "asian"]
TIMEFRAMES   = ["M1", "M5", "M15"]

SESSION_H = {"all":(0,24),"london":(7,16),"newyork":(13,21),"asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK = 0.01
MAX_HOLD_TF = {"M1":100,"M5":300,"M15":200}

# Regime codes
TREND=0; CYCLE=1; NOISE=2; TRANS=3
REGIME_NAMES = {TREND:"trend", CYCLE:"cycle", NOISE:"noise", TRANS:"trans"}

# ── Data ─────────────────────────────────────────────────────────────────────
def load_m1(zips):
    frames=[]
    for z in zips:
        with ZipFile(z) as zf:
            csv=[n for n in zf.namelist() if n.lower().endswith(".csv")][0]
            with zf.open(csv) as f:
                df=pd.read_csv(f,sep=";",header=None,
                    names=["dt","open","high","low","close","volume"],
                    dtype={"open":"f8","high":"f8","low":"f8","close":"f8","volume":"f8"})
        frames.append(df)
    df=pd.concat(frames,ignore_index=True)
    df["dt"]=pd.to_datetime(df["dt"],format="%Y%m%d %H%M%S")
    return df.sort_values("dt").drop_duplicates("dt").set_index("dt")

def resample(df,tf):
    if tf=="M1": return df.copy()
    return df.resample({"M5":"5min","M15":"15min"}[tf]).agg(
        {"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna()

def smask(idx,sess):
    # HistData usa timestamp EST (GMT-5, no DST): shift a UTC prima delle sessioni
    h=(idx.hour+5)%24; s,e=SESSION_H[sess]
    return (h>=s) if e==24 else (h>=s)&(h<e)

# ── Indicators ────────────────────────────────────────────────────────────────
def calc_atr(df,p=14):
    h,l,c=df["high"].values,df["low"].values,df["close"].values
    pc=np.roll(c,1); pc[0]=c[0]
    tr=np.maximum(h-l,np.maximum(np.abs(h-pc),np.abs(l-pc)))
    a=tr.copy(); alpha=1.0/p
    for i in range(1,len(tr)): a[i]=a[i-1]*(1-alpha)+tr[i]*alpha
    return a

def calc_ema(arr,p):
    k=2.0/(p+1); out=arr.copy()
    for i in range(1,len(arr)): out[i]=arr[i]*k+out[i-1]*(1-k)
    return out

def calc_rsi(close,p=14):
    delta=np.diff(close,prepend=close[0])
    gain=np.where(delta>0,delta,0.0)
    loss=np.where(delta<0,-delta,0.0)
    alpha=1.0/p
    ag=gain.copy(); al=loss.copy()
    for i in range(1,len(gain)):
        ag[i]=ag[i-1]*(1-alpha)+gain[i]*alpha
        al[i]=al[i-1]*(1-alpha)+loss[i]*alpha
    rs=np.where(al>0,ag/al,np.inf)
    return 100.0-100.0/(1.0+rs)

# ── Spectral regime computation ───────────────────────────────────────────────
def compute_regime(log_ret: np.ndarray, N: int,
                   delta: float, slope_thresh: float,
                   chunk_size: int = 250_000) -> np.ndarray:
    """
    Returns regime array of length T with values {TREND,CYCLE,NOISE,TRANS}.
    Uses chunked processing for large arrays (M1).
    """
    T = len(log_ret)
    hann = np.hanning(N)
    regime_full = np.full(T, TRANS, dtype=np.int8)

    n_bins_exp = N // 2 + 1
    lb = max(1, int(n_bins_exp * BAND_LO_PCT))
    hb = int(n_bins_exp * BAND_HI_PCT)
    mid_bins = np.arange(lb, hb, dtype=float)
    log_mid_bins = np.log(mid_bins)
    log_mid_bins_c = log_mid_bins - log_mid_bins.mean()
    denom = (log_mid_bins_c**2).sum()

    def _process_chunk(wins):
        F    = np.fft.rfft(wins, axis=1)
        pwr  = np.abs(F)**2
        n_b  = pwr.shape[1]
        tot  = pwr[:,1:].sum(axis=1) + 1e-30
        lb_  = max(1, int(n_b * BAND_LO_PCT))
        hb_  = int(n_b * BAND_HI_PCT)
        hb_  = max(lb_+1, min(hb_, n_b))
        mid_r = pwr[:,lb_:hb_].sum(axis=1) / tot
        hf_r  = pwr[:,hb_:].sum(axis=1) / tot
        # Spectral slope in mid+high band
        band_slice = pwr[:,lb_:]
        n_band = band_slice.shape[1]
        if n_band > 1:
            log_b = np.log(np.arange(lb_, lb_+n_band, dtype=float) + 1e-9)
            log_b_c = log_b - log_b.mean()
            log_pwr_b = np.log(band_slice + 1e-40)
            den = (log_b_c**2).sum()
            slope = (log_pwr_b * log_b_c[None,:]).sum(axis=1) / max(den, 1e-30)
        else:
            slope = np.zeros(len(wins))
        reg = np.where(slope < slope_thresh, TREND,
              np.where(mid_r > hf_r + delta, CYCLE,
              np.where(hf_r > mid_r + delta, NOISE, TRANS))).astype(np.int8)
        return reg

    if T <= chunk_size + N:
        wins = sliding_window_view(log_ret, N) * hann
        regime_full[N-1:] = _process_chunk(wins)
    else:
        step = chunk_size
        pos = 0
        while pos < T - N + 1:
            end = min(pos + step + N - 1, T)
            chunk = log_ret[pos:end]
            if len(chunk) < N: break
            wins = sliding_window_view(chunk, N) * hann
            reg = _process_chunk(wins)
            out_idx = np.arange(pos + N - 1, pos + N - 1 + len(reg))
            out_idx = out_idx[out_idx < T]
            regime_full[out_idx] = reg[:len(out_idx)]
            pos += step

    return regime_full

# ── Strategy signals ──────────────────────────────────────────────────────────
def derivative_signals(close: np.ndarray, ema_p: int = 10) -> tuple:
    """Zero-crossing of EMA first derivative."""
    ema = calc_ema(close, ema_p)
    d1  = np.diff(ema, prepend=ema[0])
    d1p = np.roll(d1, 1); d1p[0] = d1[0]
    long_s  = (d1 > 0) & (d1p <= 0)
    short_s = (d1 < 0) & (d1p >= 0)
    long_s[0] = False; short_s[0] = False
    return long_s, short_s

def rsi_signals(close: np.ndarray, p: int = 14,
                ob: float = 70.0, os_: float = 30.0) -> tuple:
    """RSI mean-reversion: cross of ob/os levels."""
    rsi = calc_rsi(close, p)
    rsi_p = np.roll(rsi, 1); rsi_p[0] = rsi[0]
    long_s  = (rsi > os_) & (rsi_p <= os_)   # cross up through oversold
    short_s = (rsi < ob)  & (rsi_p >= ob)    # cross down through overbought
    long_s[0] = False; short_s[0] = False
    return long_s, short_s

# ── Simulation ────────────────────────────────────────────────────────────────
def sim_and_metrics(entry_bars, directions, ep, sl_d, rr, high, low, max_hold):
    n = len(entry_bars)
    if n == 0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    N = len(high); mj = min(max_hold, N)
    rows = np.clip(entry_bars[:,None] + np.arange(mj)[None,:], 0, N-1)
    H = high[rows]; L = low[rows]
    tp_p = ep + directions*rr*sl_d; sl_p = ep - directions*sl_d
    li = directions==1; si = directions==-1
    tp_hit = np.zeros((n,mj),dtype=bool); sl_hit = np.zeros((n,mj),dtype=bool)
    if li.any(): tp_hit[li]=H[li]>=tp_p[li,None]; sl_hit[li]=L[li]<=sl_p[li,None]
    if si.any(): tp_hit[si]=L[si]<=tp_p[si,None]; sl_hit[si]=H[si]>=sl_p[si,None]
    tp_b = np.where(tp_hit.any(1),np.argmax(tp_hit,1),mj)
    sl_b = np.where(sl_hit.any(1),np.argmax(sl_hit,1),mj)
    # tie-break pessimistico: se TP e SL cadono nella stessa barra conta lo SL
    win  = (tp_b<sl_b)&(tp_b<mj); lose = (sl_b<=tp_b)&(sl_b<mj)
    pnl_r = np.where(win,rr,np.where(lose,-1.,0.))
    eq=1.; peak=1.; mx_dd=0.
    for r in pnl_r:
        eq*=(1+RISK*r)
        if eq>peak: peak=eq
        dd=(peak-eq)/peak*100
        if dd>mx_dd: mx_dd=dd
    tot=int(n); wins=int(win.sum())
    gp=float(pnl_r[pnl_r>0].sum()); gl=float(abs(pnl_r[pnl_r<0].sum()))
    pf=gp/gl if gl>0 else (float("inf") if gp>0 else 0.)
    return {"trades":tot,"win_rate":round(wins/tot*100,2) if tot else 0.,
            "profit_factor":round(pf,4),"max_drawdown_pct":round(mx_dd,2),
            "pnl_pct":round((eq-1)*100,2),"longs":int(li.sum()),"shorts":int(si.sum())}

def run_strategy(long_s, short_s, regime, target_regime, sess_m, valid,
                 op, atr, sl_mult, rr, high, low, max_hold, filter_on):
    """
    Combina segnale strategia + filtro regime + filtro sessione.
    Se filter_on=False -> ignora il regime (baseline).
    """
    gate = (regime == target_regime) if filter_on else np.ones(len(long_s), dtype=bool)
    act  = gate & sess_m & valid
    li   = np.where(long_s  & act)[0]
    si   = np.where(short_s & act)[0]
    all_i = np.concatenate([li, si])
    all_d = np.concatenate([np.ones(len(li)), -np.ones(len(si))])
    if len(all_i) == 0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    order = np.argsort(all_i, kind="stable")
    all_i = all_i[order]; all_d = all_d[order]
    eb  = np.minimum(all_i + 1, len(op) - 1)
    ep  = op[eb]; sl_d = sl_mult * atr[all_i]
    return sim_and_metrics(eb, all_d, ep, sl_d, rr, high, low, max_hold)

# ── Main grid ─────────────────────────────────────────────────────────────────
STRAT_PARAMS = {
    "derivative": dict(sl_mult=1.5, rr=3.0, warmup=15),
    "rsi":        dict(sl_mult=1.5, rr=2.0, warmup=20),
}
# Hypotheses to test:
# derivative → best in CYCLE (structured oscillation provides momentum)
# rsi        → best in NOISE (less structure = mean-reversion more reliable)
STRAT_REGIME = {"derivative": CYCLE, "rsi": NOISE}

def run_grid(df, tf, regime_cache):
    """
    regime_cache: dict[(N, delta, slope_thresh)] -> regime_array
    """
    close  = df["close"].values; high  = df["high"].values
    low    = df["low"].values;   op    = df["open"].values
    idx    = df.index; T = len(close)
    atr    = calc_atr(df)
    max_hold = MAX_HOLD_TF[tf]
    sm_cache = {s: smask(idx, s) for s in SESSIONS}

    # Precompute strategy signals (fixed params)
    l_der, s_der = derivative_signals(close)
    l_rsi, s_rsi = rsi_signals(close)
    sig_cache = {
        "derivative": (l_der, s_der),
        "rsi":        (l_rsi, s_rsi),
    }

    results = []

    for N, delta, slope_thresh in product(FFT_NS[tf], DELTAS, SLOPE_THRESH):
        key = (N, delta, slope_thresh)
        if key not in regime_cache:
            lr = np.diff(np.log(close), prepend=np.log(close[0]))
            regime_cache[key] = compute_regime(lr, N, delta, slope_thresh)
        regime = regime_cache[key]

        # Regime distribution stats
        dist = {REGIME_NAMES[r]: round(float((regime==r).mean()*100),1)
                for r in [TREND,CYCLE,NOISE,TRANS]}

        for strat_name, sess in product(STRAT_PARAMS.keys(), SESSIONS):
            sp     = STRAT_PARAMS[strat_name]
            tgt_r  = STRAT_REGIME[strat_name]
            ls, ss = sig_cache[strat_name]
            sm     = sm_cache[sess]
            warmup = sp["warmup"] + N
            valid  = np.zeros(T, dtype=bool); valid[warmup:] = True

            # Baseline (no regime filter)
            base = run_strategy(ls, ss, regime, tgt_r, sm, valid,
                                op, atr, sp["sl_mult"], sp["rr"],
                                high, low, max_hold, filter_on=False)
            # With regime filter
            filt = run_strategy(ls, ss, regime, tgt_r, sm, valid,
                                op, atr, sp["sl_mult"], sp["rr"],
                                high, low, max_hold, filter_on=True)

            def row(m, filtered):
                return {
                    "tf": tf, "strategy": strat_name, "fft_n": N,
                    "delta": delta, "slope_thresh": slope_thresh,
                    "session_label": sess, "regime_filter": filtered,
                    "target_regime": REGIME_NAMES[tgt_r],
                    "regime_pct": dist[REGIME_NAMES[tgt_r]],
                    **{f"regime_{k}_pct": v for k,v in dist.items()},
                    **m
                }

            results.append(row(base, "none"))
            results.append(row(filt, REGIME_NAMES[tgt_r]))

    return results

# ── Test A: forward return stats per regime (no simulation needed) ─────────────
def test_a_forward_returns(df, tf):
    """Returns dataframe with avg forward return per regime label."""
    close = df["close"].values; T = len(close)
    lr = np.diff(np.log(close), prepend=np.log(close[0]))
    records = []
    for N, delta, slope_thresh in product(FFT_NS[tf], DELTAS, SLOPE_THRESH):
        regime = compute_regime(lr, N, delta, slope_thresh)
        for h in [5, 10, 20]:
            # fwd[i] = rendimento log cumulato delle h barre SUCCESSIVE (lr[i+1..i+h]):
            # conv[j] = somma lr[j-h+1..j], quindi la somma forward da i+1 e' conv[i+h].
            # Le ultime h barre non hanno abbastanza dati futuri -> NaN (escluse da nanmean).
            conv = np.convolve(lr, np.ones(h), 'full')
            fwd = np.full(T, np.nan)
            fwd[:T-h] = conv[h:T]
            for r, rname in REGIME_NAMES.items():
                mask = (regime == r)
                n = int(mask.sum())
                if n < 10: continue
                avg = float(np.nanmean(fwd[mask])) * 10000  # pips
                std = float(np.nanstd(fwd[mask]))  * 10000
                records.append({
                    "tf": tf, "fft_n": N, "delta": delta,
                    "slope_thresh": slope_thresh, "regime": rname,
                    "horizon_bars": h, "avg_return_pip": round(avg,3),
                    "std_pip": round(std,3), "n_bars": n,
                    "regime_pct": round(n/T*100,1)
                })
    return pd.DataFrame(records)

# ── Combine & sort ────────────────────────────────────────────────────────────
def build_combined(tf, tr_list, os_list):
    key_cols = ["tf","strategy","fft_n","delta","slope_thresh",
                "session_label","regime_filter","target_regime"]
    metric_cols = ["trades","win_rate","profit_factor",
                   "max_drawdown_pct","pnl_pct","longs","shorts"]

    def pfx(rows, p):
        df = pd.DataFrame(rows)
        rename = {c: f"{p}_{c}" for c in metric_cols if c in df.columns}
        return df.rename(columns=rename)

    tr = pfx(tr_list, "train")
    os = pfx(os_list, "oos")

    # Merge solo su colonne chiave strutturali, non su stat calcolate
    merge_on = [c for c in key_cols if c in tr.columns and c in os.columns]

    # Drop duplicate non-key cols from os before merge to avoid _x/_y conflicts
    os_drop = [c for c in os.columns
               if c not in merge_on and not c.startswith("oos_")
               and c in tr.columns and not c.startswith("train_")]
    m = tr.merge(os.drop(columns=os_drop, errors="ignore"), on=merge_on, how="inner")

    # Mantieni solo le regime_*_pct dal train (valori OOS non rilevanti per il merge)
    for col in ["regime_pct","regime_trend_pct","regime_cycle_pct",
                "regime_noise_pct","regime_trans_pct"]:
        if f"{col}_x" in m.columns:
            m[col] = m[f"{col}_x"]
            m = m.drop(columns=[f"{col}_x", f"{col}_y"], errors="ignore")

    # Delta PF (OOS - Train)
    if "oos_profit_factor" in m.columns and "train_profit_factor" in m.columns:
        m["delta_pf"] = round(m["oos_profit_factor"] - m["train_profit_factor"], 4)

    # PF gain vs baseline
    base_cols = ["tf","strategy","fft_n","delta","slope_thresh","session_label"]
    base_mask = m.regime_filter == "none"
    if base_mask.any():
        base = m.loc[base_mask, base_cols +
                     ["oos_profit_factor","oos_max_drawdown_pct","oos_trades"
                      ]].rename(columns={
                         "oos_profit_factor":"base_oos_pf",
                         "oos_max_drawdown_pct":"base_oos_dd",
                         "oos_trades":"base_oos_trades"})
        m = m.merge(base, on=base_cols, how="left")
        m["pf_gain"] = round(m["oos_profit_factor"] - m["base_oos_pf"], 4)
    else:
        m["base_oos_pf"] = np.nan; m["pf_gain"] = np.nan

    return m.sort_values(["oos_profit_factor","oos_max_drawdown_pct"],
                         ascending=[False,True]).reset_index(drop=True)

# ── Report ────────────────────────────────────────────────────────────────────
def write_report(label, df, ts):
    RPT_DIR.mkdir(parents=True, exist_ok=True)
    # Best filtered results (non baseline)
    filt = df[df.regime_filter != "none"].reset_index(drop=True)
    if len(filt) == 0: return
    b = filt.iloc[0]

    lines = [f"# FFT Spectral Regime Classifier (#12) — {label}","",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_spectral_regime_filter]]","",
        f"- Generated: {ts}  |  Combos: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025","",
        "## Logica",
        "- FFT su log-return con Hann window",
        "- Regime CYCLE: mid_ratio > hf_ratio + delta",
        "- Regime NOISE: hf_ratio > mid_ratio + delta",
        "- Regime TREND: spectral_slope < slope_thresh",
        "- Derivate → filtrate da CYCLE  |  RSI → filtrate da NOISE","",
        "## Best setup filtrato",
        f"- {b['strategy'].upper()} in {b['regime_filter']} | N={int(b['fft_n'])} delta={b['delta']:.2f}",
        f"- Session={b['session_label']} | OOS PF={b['oos_profit_factor']:.3f}",
        f"- OOS DD={b['oos_max_drawdown_pct']:.1f}%  | PF Gain vs baseline={b.get('pf_gain',0):.3f}","",
        "## Top 10 filtrati","",
        "| # | Strat | Regime | N | Delta | Session | Train PF | OOS PF | OOS DD% | PF Gain |",
        "|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(filt.head(10).itertuples(index=False), 1):
        d = r._asdict()
        pg = d.get("pf_gain", 0)
        lines.append(
            f"| {i} | {d['strategy']} | {d['regime_filter']} | {int(d['fft_n'])}"
            f" | {d['delta']:.2f} | {d['session_label']}"
            f" | {d['train_profit_factor']:.3f} | {d['oos_profit_factor']:.3f}"
            f" | {d['oos_max_drawdown_pct']:.1f} | {pg:+.3f} |")

    (RPT_DIR / f"regime_report_{label.lower()}.md"
     ).write_text("\n".join(lines)+"\n", encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

    print("Loading M1 data..."); t0 = time.time()
    m1 = load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")

    all_dfs = []; all_ta = []

    for tf in TIMEFRAMES:
        print(f"\n[{tf}] resampling...")
        tf_df  = resample(m1, tf)
        train  = tf_df.loc[TRAIN_S:TRAIN_E]
        oos    = tf_df.loc[OOS_S:OOS_E]
        nc     = len(FFT_NS[tf])*len(DELTAS)*len(SLOPE_THRESH)*len(STRAT_PARAMS)*len(SESSIONS)*2
        print(f"  train={len(train)} bars  oos={len(oos)} bars  combos={nc}")

        t1 = time.time()

        # Test A: forward returns
        print("  Test A: forward return stats...")
        ta_train = test_a_forward_returns(train, tf)
        ta_oos   = test_a_forward_returns(oos,   tf)
        ta_train["split"] = "train"; ta_oos["split"] = "oos"
        all_ta.append(pd.concat([ta_train, ta_oos]))

        # Tests B+C: strategy filter
        print("  Tests B+C: strategy regime filter...")
        rc_train: dict = {}; rc_oos: dict = {}
        tr_rows = run_grid(train, tf, rc_train)
        os_rows = run_grid(oos,   tf, rc_oos)
        combined = build_combined(tf, tr_rows, os_rows)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR / f"regime_results_{tf.lower()}.csv", index=False)

        elapsed = time.time() - t1
        filt_best = combined[combined.regime_filter != "none"]
        if len(filt_best):
            b = filt_best.iloc[0]
            print(f"  {elapsed:.1f}s | best filtered: {b['strategy']} in {b['regime_filter']}"
                  f" PF={b['oos_profit_factor']:.3f} DD={b['oos_max_drawdown_pct']:.1f}%"
                  f" gain={b.get('pf_gain',0):+.3f}")

    # Save all
    ta_df = pd.concat(all_ta)
    ta_df.to_csv(OUT_DIR / "regime_test_a_forward_returns.csv", index=False)

    all_df = pd.concat(all_dfs).sort_values(
        ["oos_profit_factor","oos_max_drawdown_pct"],
        ascending=[False,True]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR / "regime_results_all.csv", index=False)
    all_df.to_json(OUT_DIR / "regime_results_all.json", orient="records", indent=2)

    write_report("ALL_TFS", all_df, ts)
    for tf in TIMEFRAMES:
        sub = all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf, sub, ts)

    print(f"\nDone. {len(all_df)} total rows.")

    # Summary print
    print("\n=== SUMMARY: filtered vs baseline ===")
    for strat in ["derivative","rsi"]:
        for tf in TIMEFRAMES:
            sub = all_df[(all_df.strategy==strat)&(all_df.tf==tf)]
            base = sub[sub.regime_filter=="none"]
            filt = sub[sub.regime_filter!="none"]
            if len(base) and len(filt):
                b_pf = base.iloc[0].oos_profit_factor
                f_pf = filt.iloc[0].oos_profit_factor
                gain = filt.iloc[0].get("pf_gain",0)
                print(f"  {strat:12s} {tf}: base_OOS_PF={b_pf:.3f}  "
                      f"best_filter_PF={f_pf:.3f}  gain={gain:+.3f}")

if __name__ == "__main__":
    main()
