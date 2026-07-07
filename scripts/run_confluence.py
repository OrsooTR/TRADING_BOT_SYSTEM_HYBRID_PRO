"""
FFT + Derivative Confluence (#17) — Vectorized Backtest
EURUSD M5/M15 | Train: 2020 | OOS: 2021-2025

Logica (compendium cap. 15):
  FFT → contesto ciclico (regime + direzione)
  Derivata → timing di entrata

Tre modalità per misurare il valore incrementale di ogni layer:
  A. baseline        : solo Derivata (d1 zero-crossing)
  B. fft_cycle_only  : Derivata + FFT cycle slope allineato (no regime gate)
  C. full_confluence : Derivata + FFT cycle slope + CYCLE regime gate (#12)

Entry:
  LONG  = d1_crosses_up  AND cycle_slope > 0 AND [in_CYCLE_regime]
  SHORT = d1_crosses_down AND cycle_slope < 0 AND [in_CYCLE_regime]
"""
from __future__ import annotations
import numpy as np, pandas as pd, os, time
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parent.parent
HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", ROOT / "data" / "histdata"))
ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
        for y in [2020,2021,2022,2023,2024,2025]]
OUT_DIR = ROOT / "artifacts" / "confluence_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "confluence_backtests" / "reports"

# ── Grid ─────────────────────────────────────────────────────────────────────
FFT_NS         = {"M5": [64, 128], "M15": [64, 128]}
DELTAS         = [0.03, 0.05, 0.08]  # soglia CYCLE regime
MIN_PERIODS    = [3, 5, 10]          # periodo minimo ciclo dominante (barre)
PWR_THRESHS    = [0.0, 0.08, 0.12]  # 0.0 = nessun filtro potenza
EMA_PERIODS    = [10, 20]
SL_MULTS       = [1.0, 1.5]
RRS            = [2.0, 3.0, 4.0]
SESSIONS       = ["all", "london", "newyork", "asian"]
TIMEFRAMES     = ["M5", "M15"]
FILTER_MODES   = ["baseline", "fft_cycle_only", "full_confluence"]
MIN_TRADES_OOS = 30                  # soglia minima per risultati validi

SESSION_H  = {"all":(0,24),"london":(7,16),"newyork":(13,21),"asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK = 0.01
MAX_HOLD_TF = {"M5":300,"M15":200}

# Bande fisse per regime (#12)
REGIME_LO_PCT = 0.10   # bins < 10% = bassa freq
REGIME_HI_PCT = 0.60   # bins > 60% = alta freq
# Bande per ciclo dominante (#11)
CYCLE_LO_PCT  = 0.05   # escludi DC e bins molto bassi
CYCLE_HI_PCT  = 0.80   # escludi rumore puro

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

# ── Combined FFT features (single pass per N) ─────────────────────────────────
def compute_fft_features(log_ret: np.ndarray, N: int) -> dict:
    """
    Computa una volta sola per N. Restituisce tutti i vettori grezzi
    che vengono poi filtrati dai parametri (delta, min_period, pwr_thresh).
    """
    T = len(log_ret)
    hann = np.hanning(N)

    # Chunked per M5 con OOS lungo
    chunk = 400_000
    if T <= chunk + N:
        wins = sliding_window_view(log_ret, N) * hann
        F    = np.fft.rfft(wins, axis=1)
        pwr  = np.abs(F)**2
        n_w  = len(wins)
    else:
        # Primo blocco: preallochiamo output
        n_w    = T - N + 1
        n_bins = N // 2 + 1
        pwr    = np.zeros((n_w, n_bins), dtype=np.float32)
        F_full = np.zeros((n_w, n_bins), dtype=np.complex64)
        pos = 0; out_pos = 0
        while pos < T - N + 1:
            end  = min(pos + chunk + N - 1, T)
            seg  = log_ret[pos:end]
            if len(seg) < N: break
            w    = sliding_window_view(seg, N) * hann
            Fc   = np.fft.rfft(w, axis=1)
            pw   = np.abs(Fc)**2
            n_   = len(w)
            pwr   [out_pos:out_pos+n_] = pw.astype(np.float32)
            F_full[out_pos:out_pos+n_] = Fc.astype(np.complex64)
            out_pos += n_; pos += chunk
        F = F_full

    n_bins  = pwr.shape[1]
    tot     = pwr[:,1:].sum(axis=1, keepdims=True)[:,0] + 1e-30

    # ── Regime (#12) — band ratios ──────────────────────────────────────────
    lb_r = max(1, int(n_bins * REGIME_LO_PCT))
    hb_r = int(n_bins * REGIME_HI_PCT)
    mid_r = pwr[:,lb_r:hb_r].sum(1) / tot
    hf_r  = pwr[:,hb_r:].sum(1)     / tot

    # ── Dominant cycle (#11) — bin dominante in banda media ─────────────────
    lo_c = max(1, int(n_bins * CYCLE_LO_PCT))
    hi_c = min(n_bins-1, int(n_bins * CYCLE_HI_PCT))

    pwr_m = pwr.copy()
    pwr_m[:,:lo_c] = 0.0
    pwr_m[:,hi_c:] = 0.0

    dom_k     = np.argmax(pwr_m, axis=1)          # (n_w,)
    rows      = np.arange(n_w)
    dom_pwr   = pwr[rows, dom_k]
    pwr_ratio = dom_pwr / tot
    dom_period = N / (dom_k.astype(float) + 1e-9)

    # Ricostruzione segnale ciclico (IFFT parziale)
    F_filt          = np.zeros_like(F)
    F_filt[rows, dom_k] = F[rows, dom_k]
    recon           = np.fft.irfft(F_filt, n=N, axis=1)[:, -1]

    # Porta tutto a lunghezza T
    def _full(arr, fill=np.nan):
        out = np.full(T, fill, dtype=np.float32)
        out[N-1:N-1+len(arr)] = arr
        return out

    mid_r_f    = _full(mid_r,    0.0)
    hf_r_f     = _full(hf_r,     0.0)
    pwr_ratio_f = _full(pwr_ratio, 0.0)
    dom_period_f = _full(dom_period, 0.0)
    recon_f    = _full(recon,    np.nan)

    # Slope del ciclo (derivata discreta)
    slope_f = np.diff(recon_f.astype(float), prepend=np.nan).astype(np.float32)

    return {
        "mid_r":      mid_r_f,
        "hf_r":       hf_r_f,
        "pwr_ratio":  pwr_ratio_f,
        "dom_period": dom_period_f,
        "slope":      slope_f,
        "warmup":     N,
    }

# ── Simulation ────────────────────────────────────────────────────────────────
def sim_and_metrics(eb, all_d, ep, sl_d, rr, high, low, max_hold):
    n=len(eb)
    if n==0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    N=len(high); mj=min(max_hold,N)
    rows=np.clip(eb[:,None]+np.arange(mj)[None,:],0,N-1)
    H=high[rows]; L=low[rows]
    li=all_d==1; si=all_d==-1
    tp_p=ep+all_d*rr*sl_d; sl_p=ep-all_d*sl_d
    tp_hit=np.zeros((n,mj),dtype=bool); sl_hit=np.zeros((n,mj),dtype=bool)
    if li.any(): tp_hit[li]=H[li]>=tp_p[li,None]; sl_hit[li]=L[li]<=sl_p[li,None]
    if si.any(): tp_hit[si]=L[si]<=tp_p[si,None]; sl_hit[si]=H[si]>=sl_p[si,None]
    tp_b=np.where(tp_hit.any(1),np.argmax(tp_hit,1),mj)
    sl_b=np.where(sl_hit.any(1),np.argmax(sl_hit,1),mj)
    # tie-break pessimistico: se TP e SL cadono nella stessa barra conta lo SL
    win=(tp_b<sl_b)&(tp_b<mj); lose=(sl_b<=tp_b)&(sl_b<mj)
    pnl_r=np.where(win,rr,np.where(lose,-1.,0.))
    eq=1.; peak=1.; mx_dd=0.
    for r in pnl_r:
        eq*=(1+RISK*r)
        if eq>peak: peak=eq
        dd=(peak-eq)/peak*100
        if dd>mx_dd: mx_dd=dd
    tot=int(n); wins=int(win.sum())
    gp=float(pnl_r[pnl_r>0].sum()); gl=float(abs(pnl_r[pnl_r<0].sum()))
    pf=gp/gl if gl>0 else (float("inf") if gp>0 else 0.)
    return {"trades":tot,"win_rate":round(wins/tot*100,2),
            "profit_factor":round(pf,4),"max_drawdown_pct":round(mx_dd,2),
            "pnl_pct":round((eq-1)*100,2),"longs":int(li.sum()),"shorts":int(si.sum())}

def run_signals(ls, ss, gate, sm, valid, op, atr, sl_mult, rr, high, low, mh):
    act=gate & sm & valid
    li=np.where(ls & act)[0]; si=np.where(ss & act)[0]
    all_i=np.concatenate([li,si]); all_d=np.concatenate([np.ones(len(li)),-np.ones(len(si))])
    if len(all_i)==0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    order=np.argsort(all_i,kind="stable")
    all_i=all_i[order]; all_d=all_d[order]
    eb=np.minimum(all_i+1,len(op)-1)
    return sim_and_metrics(eb, all_d, op[eb], sl_mult*atr[all_i], rr, high, low, mh)

# ── Main grid ─────────────────────────────────────────────────────────────────
PARAM_COLS = ["tf","filter_mode","fft_n","delta","min_period","pwr_thresh",
              "ema_period","sl_atr_mult","rr","session_label"]

def run_grid(df, tf, fft_cache: dict) -> list[dict]:
    close=df["close"].values; high=df["high"].values
    low=df["low"].values;     op=df["open"].values
    idx=df.index; T=len(close)
    atr=calc_atr(df); mh=MAX_HOLD_TF[tf]
    lr=np.diff(np.log(close), prepend=np.log(close[0]))
    sm_cache={s:smask(idx,s) for s in SESSIONS}

    # Precompute FFT features per N (single pass)
    for N in FFT_NS[tf]:
        if N not in fft_cache:
            fft_cache[N] = compute_fft_features(lr, N)

    results = []

    for ema_p in EMA_PERIODS:
        # Derivata (unico calcolo per ema_p)
        ema = calc_ema(close, ema_p)
        d1  = np.diff(ema, prepend=ema[0])
        d1p = np.roll(d1, 1); d1p[0] = d1[0]
        ls_d = (d1 > 0) & (d1p <= 0); ls_d[0] = False
        ss_d = (d1 < 0) & (d1p >= 0); ss_d[0] = False

        for sl_m, rr, sess in product(SL_MULTS, RRS, SESSIONS):
            sm = sm_cache[sess]
            warmup_base = max(ema_p, 14) + 1
            valid_base = np.zeros(T, dtype=bool); valid_base[warmup_base:] = True

            # BASELINE: solo derivata
            m = run_signals(ls_d, ss_d, valid_base, sm, valid_base,
                            op, atr, sl_m, rr, high, low, mh)
            results.append({**dict(zip(PARAM_COLS,
                [tf,"baseline",0,0.,0,0.,ema_p,sl_m,rr,sess])), **m,
                "trade_reduction_pct":0., "regime_pct":0.})

            # FFT-enhanced modes
            for N, delta, min_per, pwr_t in product(
                    FFT_NS[tf], DELTAS, MIN_PERIODS, PWR_THRESHS):
                feat = fft_cache[N]
                warmup = max(warmup_base, feat["warmup"] + 2)
                valid  = np.zeros(T, dtype=bool); valid[warmup:] = True

                slope = feat["slope"]
                pr    = feat["pwr_ratio"]
                dom_p = feat["dom_period"]
                mid_r = feat["mid_r"]
                hf_r  = feat["hf_r"]

                # Quality: ciclo dominante affidabile
                quality = (pr >= pwr_t) & (dom_p >= min_per)

                # Direzione FFT concorda con derivata
                long_fft  = ls_d & quality & (slope > 0)
                short_fft = ss_d & quality & (slope < 0)

                # Regime CYCLE gate
                in_cycle = (mid_r > hf_r + delta)
                long_full  = long_fft  & in_cycle
                short_full = short_fft & in_cycle

                # Conteggio trade previsto (per trade_reduction_pct vs baseline)
                n_base = (ls_d | ss_d).sum()
                n_full = (long_full | short_full).sum()
                tr_pct = round(float((1 - n_full/max(n_base,1))*100), 1)
                cyc_pct = round(float(in_cycle.mean()*100), 1)

                row_base = dict(zip(PARAM_COLS,
                    [tf, "", N, delta, min_per, pwr_t, ema_p, sl_m, rr, sess]))

                # Mode B: FFT cycle direction only
                m = run_signals(long_fft, short_fft, valid, sm, valid,
                                op, atr, sl_m, rr, high, low, mh)
                results.append({**row_base,
                    "filter_mode":"fft_cycle_only", **m,
                    "trade_reduction_pct":tr_pct, "regime_pct":cyc_pct})

                # Mode C: full confluence
                m = run_signals(long_full, short_full, valid, sm, valid,
                                op, atr, sl_m, rr, high, low, mh)
                results.append({**row_base,
                    "filter_mode":"full_confluence", **m,
                    "trade_reduction_pct":tr_pct, "regime_pct":cyc_pct})

    return results

# ── Combine & sort ────────────────────────────────────────────────────────────
def build_combined(tf, tr_list, os_list):
    key    = PARAM_COLS   # structural parameters only
    metric = ["trades","win_rate","profit_factor","max_drawdown_pct","pnl_pct","longs","shorts"]
    extra  = ["trade_reduction_pct","regime_pct"]

    def pfx(rows, p):
        df = pd.DataFrame(rows)
        return df.rename(columns={c: f"{p}_{c}" for c in metric if c in df.columns})

    tr = pfx(tr_list, "train")
    os = pfx(os_list, "oos")

    # Merge ONLY on structural param columns — not on computed stats (regime_pct etc.)
    merge_on = [c for c in key if c in tr.columns and c in os.columns]

    # Drop non-key, non-metric columns from os before merge to avoid _x/_y
    os_drop = [c for c in os.columns
               if c not in merge_on and not c.startswith("oos_")
               and c in tr.columns and not c.startswith("train_")]
    m = tr.merge(os.drop(columns=os_drop, errors="ignore"), on=merge_on, how="inner")

    # Fix duplicate extra columns (_x suffix from train side)
    for col in extra:
        if f"{col}_x" in m.columns:
            m[col] = m[f"{col}_x"]
            m = m.drop(columns=[f"{col}_x", f"{col}_y"], errors="ignore")

    if "oos_profit_factor" in m.columns and "train_profit_factor" in m.columns:
        m["delta_pf"] = round(m["oos_profit_factor"] - m["train_profit_factor"], 4)

    # PF gain vs baseline (same ema, sl, rr, session)
    base_key = ["tf","ema_period","sl_atr_mult","rr","session_label"]
    base_key = [c for c in base_key if c in m.columns]
    base = m[m.filter_mode == "baseline"][
        base_key + ["oos_profit_factor","oos_max_drawdown_pct","oos_trades"]
    ].rename(columns={"oos_profit_factor":"base_pf",
                      "oos_max_drawdown_pct":"base_dd",
                      "oos_trades":"base_trades"})
    m = m.merge(base, on=base_key, how="left")
    m["pf_gain"] = round(m["oos_profit_factor"] - m["base_pf"], 4)
    m["dd_gain"]  = round(m["base_dd"] - m["oos_max_drawdown_pct"], 4)

    # Separa validi (trade sufficienti) da outlier statistici
    m["statistically_valid"] = m["oos_trades"] >= MIN_TRADES_OOS

    return m.sort_values(
        ["statistically_valid","oos_profit_factor","oos_max_drawdown_pct"],
        ascending=[False, False, True]).reset_index(drop=True)

# ── Report ────────────────────────────────────────────────────────────────────
def write_report(label, df, ts):
    RPT_DIR.mkdir(parents=True, exist_ok=True)
    conf = df[(df.filter_mode=="full_confluence") &
              (df.get("statistically_valid", pd.Series([True]*len(df))) == True)
              ].reset_index(drop=True)
    if "statistically_valid" in df.columns:
        conf = df[(df.filter_mode=="full_confluence") & (df["statistically_valid"]==True)].reset_index(drop=True)
    if not len(conf): return
    b = conf.iloc[0]
    lines = [f"# FFT + Derivative Confluence (#17) — {label}", "",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_derivative_confluence]]", "",
        f"- Generated: {ts}  |  Combos: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025", "",
        "## Logica",
        "- **#12 FFT Regime**: CYCLE quando mid_ratio > hf_ratio + delta",
        "- **#11 FFT Cycle**: slope del ciclo dominante (direzione)",
        "- **#02 Derivata**: d1 zero-crossing (trigger di entrata)",
        "- LONG = d1↑ AND slope>0 AND CYCLE_regime",
        "- SHORT = d1↓ AND slope<0 AND CYCLE_regime",
        "- Entry: next-bar open | SL: sl_mult×ATR(14) | TP: SL×rr", "",
        "## Best Full Confluence Setup",
        f"- TF={b.get('tf')}  N={int(b['fft_n'])}  delta={b['delta']:.2f}",
        f"- min_period={int(b['min_period'])}b  pwr_thresh={b['pwr_thresh']:.2f}",
        f"- ema_period={int(b['ema_period'])}  sl={b['sl_atr_mult']:.1f}  rr={b['rr']:.1f}",
        f"- Session={b['session_label']}",
        f"- Train PF={b['train_profit_factor']:.4f} | OOS PF={b['oos_profit_factor']:.4f}",
        f"- OOS DD={b['oos_max_drawdown_pct']:.2f}%  |  OOS P&L={b['oos_pnl_pct']:.2f}%",
        f"- Trades={int(b['oos_trades'])}  Reduction={b['trade_reduction_pct']:.1f}%",
        f"- PF Gain vs baseline={b.get('pf_gain',0):+.3f}  DD Gain={b.get('dd_gain',0):+.3f}", "",
        "## Top 15 Full Confluence", "",
        "| # | TF | N | δ | minP | pwrT | EMA | SL | RR | Sess | Train PF | OOS PF | OOS DD% | Trades | PF Gain |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(conf.head(15).itertuples(index=False), 1):
        d = r._asdict()
        lines.append(
            f"| {i} | {d.get('tf','')} | {int(d['fft_n'])} | {d['delta']:.2f}"
            f" | {int(d['min_period'])} | {d['pwr_thresh']:.2f} | {int(d['ema_period'])}"
            f" | {d['sl_atr_mult']:.1f} | {d['rr']:.1f} | {d['session_label']}"
            f" | {d['train_profit_factor']:.3f} | {d['oos_profit_factor']:.3f}"
            f" | {d['oos_max_drawdown_pct']:.1f} | {int(d['oos_trades'])}"
            f" | {d.get('pf_gain',0):+.3f} |")
    (RPT_DIR / f"confluence_report_{label.lower()}.md"
     ).write_text("\n".join(lines) + "\n", encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("Loading M1 data..."); t0 = time.time()
    m1 = load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")

    all_dfs = []
    n_fft   = len(FFT_NS["M15"]) * len(DELTAS) * len(MIN_PERIODS) * len(PWR_THRESHS)
    n_combo = (1 + n_fft * 2) * len(EMA_PERIODS) * len(SL_MULTS) * len(RRS) * len(SESSIONS)

    for tf in TIMEFRAMES:
        print(f"\n[{tf}] resampling...")
        tf_df = resample(m1, tf)
        train = tf_df.loc[TRAIN_S:TRAIN_E]
        oos   = tf_df.loc[OOS_S:OOS_E]
        print(f"  train={len(train)} bars  oos={len(oos)} bars  combos≈{n_combo}")
        t1 = time.time()

        cc_tr = {}; cc_os = {}
        tr_rows = run_grid(train, tf, cc_tr)
        os_rows = run_grid(oos,   tf, cc_os)
        combined = build_combined(tf, tr_rows, os_rows)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR / f"confluence_results_{tf.lower()}.csv", index=False)

        elapsed = time.time() - t1
        conf = combined[combined.filter_mode == "full_confluence"]
        if len(conf):
            b = conf.iloc[0]
            print(f"  {elapsed:.1f}s | best: N={int(b['fft_n'])} δ={b['delta']:.2f}"
                  f" ema={int(b['ema_period'])} {b['session_label']}"
                  f" OOS_PF={b['oos_profit_factor']:.3f}"
                  f" gain={b.get('pf_gain',0):+.3f}"
                  f" trades={int(b['oos_trades'])}")

    all_df = pd.concat(all_dfs).sort_values(
        ["oos_profit_factor","oos_max_drawdown_pct"],
        ascending=[False,True]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR / "confluence_results_all.csv", index=False)
    all_df.to_json(OUT_DIR / "confluence_results_all.json", orient="records", indent=2)
    write_report("ALL_TFS", all_df, ts)
    for tf in TIMEFRAMES:
        sub = all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf, sub, ts)

    print(f"\nDone. {len(all_df)} rows.")
    print("\n=== SUMMARY ===")
    for tf in TIMEFRAMES:
        for mode in FILTER_MODES:
            sub = all_df[(all_df["tf"]==tf) & (all_df["filter_mode"]==mode)]
            # prefer rows with enough trades
            sub_valid = sub[sub["statistically_valid"]==True] if "statistically_valid" in sub.columns else sub
            sub_show = sub_valid if len(sub_valid) else sub
            if len(sub_show):
                b = sub_show.iloc[0]
                pf_g = b.get("pf_gain", 0) if b.get("pf_gain") is not None else 0
                print(f"  {tf} {mode:18s}: OOS_PF={b['oos_profit_factor']:.3f}"
                      f"  DD={b['oos_max_drawdown_pct']:.1f}%"
                      f"  trades={int(b['oos_trades'])}"
                      f"  gain={pf_g:+.3f}"
                      f"  {'✓' if b.get('statistically_valid',True) else '(few trades)'}")

if __name__ == "__main__":
    main()
