"""
Fractal + FFT Confluence (#18) — Vectorized Backtest
EURUSD M1/M5 | Train: 2020 | OOS: 2021-2025

Logica (compendium cap. 15 — "terzo layer"):
  #05 Fractal S/R → livelli di supporto/resistenza attivi (geometria)
  #11 FFT Cycle   → slope del ciclo dominante (direzione ciclica)
  #12 FFT Regime  → regime CYCLE (qualità strutturale)

Tre modalità per misurare il valore incrementale:
  baseline      : solo Fractal bounce (baseline #05)
  fft_cycle     : Fractal + FFT cycle slope allineato
  full_confl    : Fractal + FFT cycle slope + CYCLE regime gate

LONG  = bounce da supporto  AND slope_ciclo > 0 AND [regime=CYCLE]
SHORT = bounce da resistenza AND slope_ciclo < 0 AND [regime=CYCLE]
"""
from __future__ import annotations
import numpy as np, pandas as pd, os, time
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", ROOT / "data" / "histdata"))
ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
        for y in [2020,2021,2022,2023,2024,2025]]
OUT_DIR = ROOT / "artifacts" / "fractal_fft_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "fractal_fft_backtests" / "reports"
COMBINED_CSV = ROOT / "artifacts" / "derivative_backtests" / "data" / "eurusd_m1_2020_2025_combined.csv"

# ── Grid ─────────────────────────────────────────────────────────────────────
FP_VALUES    = [5]           # fractal period (best da #05)
TOL_VALUES   = [0.3, 0.5, 1.0]  # tolleranza in × ATR
LB_VALUES    = [30, 70]     # lookback barre per S/R attivi
RR_VALUES    = [2.0, 3.0]
SL_MULT      = 1.5          # fisso (best da #05)
FFT_NS       = {"M1": [64], "M5": [64, 128]}
DELTAS       = [0.03, 0.05]    # regime CYCLE gate
MIN_PERIODS  = [5, 10]
SESSIONS     = ["all", "london", "newyork", "asian"]
TIMEFRAMES   = ["M1", "M5"]
FILTER_MODES = ["baseline", "fft_cycle", "full_confl"]
MIN_TRADES   = 100

SESSION_H = {"all":(0,24),"london":(7,16),"newyork":(13,21),"asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK = 0.01
SPREAD_PIP = float(os.environ.get("SPREAD_PIP", "0.5"))  # costo spread round-trip in pip
SPREAD = SPREAD_PIP * 1e-4
MAX_HOLD_TF = {"M1": 20, "M5": 60}   # barre massime per trade

# Bande FFT (identiche a #11/#12)
REGIME_LO_PCT = 0.10
REGIME_HI_PCT = 0.60
CYCLE_LO_PCT  = 0.05
CYCLE_HI_PCT  = 0.80

PARAM_COLS = ["tf","filter_mode","fp","tol","lb","fft_n","delta",
              "min_period","rr","session_label"]

# ── Data ─────────────────────────────────────────────────────────────────────
def load_m1(zips):
    if not all(z.exists() for z in zips):
        # fallback: CSV combinato locale (stesso formato EST degli zip HistData)
        df = pd.read_csv(COMBINED_CSV, parse_dates=["datetime"], index_col="datetime")
        df = df.sort_index()
        return df[~df.index.duplicated()]
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
    return df.resample({"M5":"5min"}[tf]).agg(
        {"open":"first","high":"max","low":"min","close":"last","volume":"sum"}).dropna()

def smask(idx,sess):
    # HistData usa timestamp EST (GMT-5, no DST): shift a UTC prima delle sessioni
    h=(idx.hour+5)%24; s,e=SESSION_H[sess]
    return (h>=s) if e==24 else (h>=s)&(h<e)

# ── Indicators ────────────────────────────────────────────────────────────────
def calc_atr(high,low,close,p=14):
    pc=np.roll(close,1); pc[0]=close[0]
    tr=np.maximum(high-low,np.maximum(np.abs(high-pc),np.abs(low-pc)))
    a=tr.copy(); alpha=1.0/p
    for i in range(1,len(tr)): a[i]=a[i-1]*(1-alpha)+tr[i]*alpha
    return a

# ── Fractal pivot detection (vectorized, no lookahead) ────────────────────────
def detect_pivots(high: np.ndarray, low: np.ndarray, fp: int) -> tuple:
    """
    Returns (ph_center, pl_center): boolean arrays.
    ph_center[i]=True: high[i] è un pivot high confermato alla barra i+fp.
    No lookahead: quando siamo alla barra i+fp, conosciamo high[i-fp:i+fp+1].
    """
    T = len(high)
    win = 2*fp + 1
    ph_win = sliding_window_view(high, win).max(axis=1)  # (T-win+1,)
    pl_win = sliding_window_view(low,  win).min(axis=1)
    ph = np.zeros(T, dtype=bool)
    pl = np.zeros(T, dtype=bool)
    # center of window at index fp → global index fp+i
    c_high = high[fp:T-fp]; c_low = low[fp:T-fp]
    ph[fp:T-fp] = (c_high == ph_win) & \
                  (c_high > high[fp-1:T-fp-1]) & \
                  (c_high > high[fp+1:T-fp+1])
    pl[fp:T-fp] = (c_low  == pl_win) & \
                  (c_low  < low[fp-1:T-fp-1]) & \
                  (c_low  < low[fp+1:T-fp+1])
    return ph, pl

# ── Fractal bounce signals ────────────────────────────────────────────────────
def fractal_bounce_signals(high, low, close, atr, ph, pl, fp, tol, lb):
    """
    LONG : price touches a support level from above (pivot low)
    SHORT: price touches a resistance level from below (pivot high)
    Signal available from bar j+fp onward (confirmed pivot).
    """
    T = len(close)
    long_s  = np.zeros(T, dtype=bool)
    short_s = np.zeros(T, dtype=bool)
    ph_idx = np.where(ph)[0]
    pl_idx = np.where(pl)[0]
    for i in ph_idx:   # resistance levels
        j0 = i + fp; j1 = min(i + fp + lb, T)
        if j0 >= T: continue
        val = high[i]; c_sl = close[j0:j1]; thr = tol * atr[j0:j1]
        short_s[j0:j1] |= (np.abs(c_sl - val) <= thr) & (c_sl <= val)
    for i in pl_idx:   # support levels
        j0 = i + fp; j1 = min(i + fp + lb, T)
        if j0 >= T: continue
        val = low[i]; c_sl = close[j0:j1]; thr = tol * atr[j0:j1]
        long_s[j0:j1]  |= (np.abs(c_sl - val) <= thr) & (c_sl >= val)
    return long_s, short_s

# ── FFT features (same as #17) ────────────────────────────────────────────────
def compute_fft_features(log_ret: np.ndarray, N: int) -> dict:
    T = len(log_ret)
    hann = np.hanning(N)
    chunk = 300_000
    n_bins = N // 2 + 1

    if T <= chunk + N:
        wins = sliding_window_view(log_ret, N) * hann
        F    = np.fft.rfft(wins, axis=1)
        pwr  = np.abs(F)**2
    else:
        pwr = np.zeros((T-N+1, n_bins), dtype=np.float32)
        F   = np.zeros((T-N+1, n_bins), dtype=np.complex64)
        pos = 0; op = 0
        while pos < T - N + 1:
            end = min(pos + chunk + N - 1, T)
            seg = log_ret[pos:end]
            if len(seg) < N: break
            w = sliding_window_view(seg, N) * hann
            Fc = np.fft.rfft(w, axis=1).astype(np.complex64)
            pw = np.abs(Fc)**2
            n_ = len(w)
            pwr[op:op+n_] = pw; F[op:op+n_] = Fc
            op += n_; pos += chunk

    tot  = pwr[:,1:].sum(1) + 1e-30
    # Regime bands
    lb_r = max(1, int(n_bins*REGIME_LO_PCT))
    hb_r = int(n_bins*REGIME_HI_PCT)
    mid_r = pwr[:,lb_r:hb_r].sum(1) / tot
    hf_r  = pwr[:,hb_r:].sum(1) / tot
    # Dominant cycle
    lo_c = max(1, int(n_bins*CYCLE_LO_PCT))
    hi_c = min(n_bins-1, int(n_bins*CYCLE_HI_PCT))
    pm = pwr.copy(); pm[:,:lo_c]=0; pm[:,hi_c:]=0
    dom_k = np.argmax(pm, axis=1)
    rows  = np.arange(len(dom_k))
    pwr_ratio = pwr[rows, dom_k] / tot
    dom_per   = N / (dom_k.astype(float) + 1e-9)
    F_filt = np.zeros_like(F); F_filt[rows, dom_k] = F[rows, dom_k]
    recon  = np.fft.irfft(F_filt, n=N, axis=1)[:, -1]

    def _full(arr, fill=np.nan):
        out = np.full(T, fill, dtype=np.float32)
        out[N-1:N-1+len(arr)] = arr; return out

    recon_f = _full(recon, np.nan)
    slope_f = np.diff(recon_f.astype(float), prepend=np.nan).astype(np.float32)
    return {
        "mid_r":      _full(mid_r, 0.0),
        "hf_r":       _full(hf_r,  0.0),
        "pwr_ratio":  _full(pwr_ratio, 0.0),
        "dom_period": _full(dom_per, 0.0),
        "slope":      slope_f,
        "warmup":     N,
    }

# ── Simulation ────────────────────────────────────────────────────────────────
def sim_and_metrics(eb, all_d, ep, sl_d, rr, high, low, close, max_hold):
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
    # timeout: chiusura mark-to-market sull'ultima barra simulata invece di 0R
    last_bar=np.minimum(eb+mj-1,N-1)
    mtm_r=all_d*(close[last_bar]-ep)/np.maximum(sl_d,1e-12)
    pnl_r=np.where(win,rr,np.where(lose,-1.,np.clip(mtm_r,-1.,rr)))
    # costo spread per trade espresso in R (spread / distanza SL)
    pnl_r=pnl_r-SPREAD/np.maximum(sl_d,1e-12)
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

def run_signals(ls, ss, gate, sm, valid, op, atr, rr, high, low, close, mh):
    act = gate & sm & valid
    li=np.where(ls&act)[0]; si=np.where(ss&act)[0]
    all_i=np.concatenate([li,si]); all_d=np.concatenate([np.ones(len(li)),-np.ones(len(si))])
    if len(all_i)==0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    order=np.argsort(all_i,kind="stable")
    all_i=all_i[order]; all_d=all_d[order]
    eb=np.minimum(all_i+1,len(op)-1)
    return sim_and_metrics(eb,all_d,op[eb],SL_MULT*atr[all_i],rr,high,low,close,mh)

# ── Main grid ─────────────────────────────────────────────────────────────────
def run_grid(df, tf, fft_cache: dict) -> list[dict]:
    close=df["close"].values; high=df["high"].values
    low=df["low"].values;     op=df["open"].values
    idx=df.index; T=len(close)
    atr=calc_atr(high,low,close); mh=MAX_HOLD_TF[tf]
    lr=np.diff(np.log(close),prepend=np.log(close[0]))
    sm_cache={s:smask(idx,s) for s in SESSIONS}
    no_gate=np.ones(T,dtype=bool)

    # Cache FFT features per N
    for N in FFT_NS[tf]:
        if N not in fft_cache:
            fft_cache[N]=compute_fft_features(lr,N)

    results=[]
    # Outer: fractal params (compute signals once per combo)
    for fp,tol,lb in product(FP_VALUES, TOL_VALUES, LB_VALUES):
        ph,pl=detect_pivots(high,low,fp)
        ls_frac,ss_frac=fractal_bounce_signals(high,low,close,atr,ph,pl,fp,tol,lb)
        warmup_frac=fp*2+lb+2
        valid_frac=np.zeros(T,dtype=bool); valid_frac[warmup_frac:]=True

        for rr, sess in product(RR_VALUES, SESSIONS):
            sm=sm_cache[sess]
            base_row={"tf":tf,"fp":fp,"tol":tol,"lb":lb,"rr":rr,"session_label":sess}

            # BASELINE
            m=run_signals(ls_frac,ss_frac,no_gate,sm,valid_frac,op,atr,rr,high,low,close,mh)
            results.append({**base_row,"filter_mode":"baseline",
                            "fft_n":0,"delta":0.,"min_period":0,"fft_pct":0.,**m})

            # FFT-enhanced modes
            for N,delta,min_per in product(FFT_NS[tf],DELTAS,MIN_PERIODS):
                feat=fft_cache[N]
                slope=feat["slope"]; mid_r=feat["mid_r"]; hf_r=feat["hf_r"]
                dom_p=feat["dom_period"]
                warmup=max(warmup_frac, feat["warmup"]+2)
                valid=np.zeros(T,dtype=bool); valid[warmup:]=True
                quality=(dom_p>=min_per)
                in_cycle=(mid_r>hf_r+delta)
                fft_pct=round(float(in_cycle.mean()*100),1)

                l_fft=ls_frac & quality & (slope>0)
                s_fft=ss_frac & quality & (slope<0)
                l_full=l_fft & in_cycle
                s_full=s_fft & in_cycle

                fft_row={**base_row,"fft_n":N,"delta":delta,"min_period":min_per,"fft_pct":fft_pct}

                m=run_signals(l_fft,s_fft,no_gate,sm,valid,op,atr,rr,high,low,close,mh)
                results.append({**fft_row,"filter_mode":"fft_cycle",**m})

                m=run_signals(l_full,s_full,no_gate,sm,valid,op,atr,rr,high,low,close,mh)
                results.append({**fft_row,"filter_mode":"full_confl",**m})

    return results

# ── Combine & sort ────────────────────────────────────────────────────────────
def build_combined(tf, tr_list, os_list):
    key=PARAM_COLS
    metric=["trades","win_rate","profit_factor","max_drawdown_pct","pnl_pct","longs","shorts"]
    extra=["fft_pct"]
    def pfx(rows,p):
        df=pd.DataFrame(rows)
        return df.rename(columns={c:f"{p}_{c}" for c in metric if c in df.columns})
    tr=pfx(tr_list,"train"); os=pfx(os_list,"oos")
    merge_on=[c for c in key if c in tr.columns and c in os.columns]
    os_drop=[c for c in os.columns if c not in merge_on and not c.startswith("oos_")
             and c in tr.columns and not c.startswith("train_")]
    m=tr.merge(os.drop(columns=os_drop,errors="ignore"),on=merge_on,how="inner")
    for col in extra:
        if f"{col}_x" in m.columns:
            m[col]=m[f"{col}_x"]; m=m.drop(columns=[f"{col}_x",f"{col}_y"],errors="ignore")
    if "oos_profit_factor" in m.columns and "train_profit_factor" in m.columns:
        m["delta_pf"]=round(m["oos_profit_factor"]-m["train_profit_factor"],4)
    bk=["tf","fp","tol","lb","rr","session_label"]
    base=m[m.filter_mode=="baseline"][bk+["oos_profit_factor","oos_max_drawdown_pct","oos_trades"]]
    base=base.rename(columns={"oos_profit_factor":"base_pf","oos_max_drawdown_pct":"base_dd",
                               "oos_trades":"base_trades"})
    m=m.merge(base,on=bk,how="left")
    m["pf_gain"]=round(m["oos_profit_factor"]-m["base_pf"],4)
    m["dd_gain"]=round(m["base_dd"]-m["oos_max_drawdown_pct"],4)
    m["valid"]=(m["oos_trades"]>=MIN_TRADES)
    return m.sort_values(["valid","oos_profit_factor","oos_max_drawdown_pct"],
                         ascending=[False,False,True]).reset_index(drop=True)

# ── Report ────────────────────────────────────────────────────────────────────
def write_report(label, df, ts):
    RPT_DIR.mkdir(parents=True, exist_ok=True)
    conf=df[(df.filter_mode=="full_confl")&(df.get("valid",True)==True) if "valid" not in df.columns
            else (df.filter_mode=="full_confl")&(df["valid"]==True)].reset_index(drop=True)
    if not len(conf): conf=df[df.filter_mode=="full_confl"].reset_index(drop=True)
    if not len(conf): return
    b=conf.iloc[0]
    lines=[f"# Fractal + FFT Confluence (#18) — {label}","",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fractal_fft_pattern_projection]]","",
        f"- Generated: {ts}  |  Combos totali: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025","",
        "## Logica",
        "- **#05 Fractal S/R**: pivot Williams → livelli attivi nella finestra lookback",
        "- **#11 FFT Cycle**: slope del ciclo dominante concorda con il bounce",
        "- **#12 FFT Regime**: regime CYCLE come gate opzionale (full_confl)",
        "- LONG = bounce da supporto AND slope>0 AND [regime=CYCLE]","",
        f"## Best Full Confluence (≥{MIN_TRADES} trade OOS)",
        f"- TF={b.get('tf','')}  fp={int(b['fp'])}  tol={b['tol']:.1f}  lb={int(b['lb'])}",
        f"- N={int(b['fft_n'])}  delta={b['delta']:.2f}  min_p={int(b['min_period'])}",
        f"- RR={b['rr']:.1f}  Session={b['session_label']}",
        f"- Train PF={b['train_profit_factor']:.4f} | OOS PF={b['oos_profit_factor']:.4f}",
        f"- OOS DD={b['oos_max_drawdown_pct']:.2f}%  OOS Trades={int(b['oos_trades'])}",
        f"- PF Gain={b.get('pf_gain',0):+.3f}  DD Gain={b.get('dd_gain',0):+.3f}","",
        "## Top 15 Full Confl","",
        "| # | TF | fp | tol | lb | N | δ | Sess | RR | Train PF | OOS PF | OOS DD% | Trades | PF Gain |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i,r in enumerate(conf.head(15).itertuples(index=False),1):
        d=r._asdict()
        lines.append(f"| {i} | {d.get('tf','')} | {int(d['fp'])} | {d['tol']:.1f} | {int(d['lb'])}"
            f" | {int(d['fft_n'])} | {d['delta']:.2f} | {d['session_label']} | {d['rr']:.1f}"
            f" | {d['train_profit_factor']:.3f} | {d['oos_profit_factor']:.3f}"
            f" | {d['oos_max_drawdown_pct']:.1f} | {int(d['oos_trades'])}"
            f" | {d.get('pf_gain',0):+.3f} |")
    (RPT_DIR/f"fractal_fft_report_{label.lower()}.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("Loading M1 data..."); t0=time.time()
    m1=load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")
    all_dfs=[]
    for tf in TIMEFRAMES:
        print(f"\n[{tf}] resampling...")
        tf_df=resample(m1,tf)
        train=tf_df.loc[TRAIN_S:TRAIN_E]; oos=tf_df.loc[OOS_S:OOS_E]
        n_fractal=len(FP_VALUES)*len(TOL_VALUES)*len(LB_VALUES)
        n_fft=len(FFT_NS[tf])*len(DELTAS)*len(MIN_PERIODS)
        n_combo=n_fractal*(1+n_fft*2)*len(RR_VALUES)*len(SESSIONS)
        print(f"  train={len(train)} oos={len(oos)} combos≈{n_combo}")
        t1=time.time()
        cc_tr={}; cc_os={}
        tr_rows=run_grid(train,tf,cc_tr)
        os_rows=run_grid(oos,tf,cc_os)
        combined=build_combined(tf,tr_rows,os_rows)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR/f"fractal_fft_results_{tf.lower()}.csv",index=False)
        elapsed=time.time()-t1
        conf=combined[(combined.filter_mode=="full_confl")&(combined.get("valid",True)==True if
                      "valid" not in combined.columns else combined["valid"]==True)]
        if len(conf):
            b=conf.iloc[0]
            pg=b.get("pf_gain",0)
            print(f"  {elapsed:.1f}s | best confl: fp={int(b['fp'])} tol={b['tol']:.1f}"
                  f" {b['session_label']} OOS_PF={b['oos_profit_factor']:.3f}"
                  f" gain={pg:+.3f} trades={int(b['oos_trades'])}")

    all_df=pd.concat(all_dfs).sort_values(["valid","oos_profit_factor","oos_max_drawdown_pct"],
                                           ascending=[False,False,True]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR/"fractal_fft_results_all.csv",index=False)
    all_df.to_json(OUT_DIR/"fractal_fft_results_all.json",orient="records",indent=2)
    write_report("ALL_TFS",all_df,ts)
    for tf in TIMEFRAMES:
        sub=all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf,sub,ts)

    print(f"\nDone. {len(all_df)} rows.")
    print("\n=== SUMMARY per layer ===")
    for tf in TIMEFRAMES:
        for mode in FILTER_MODES:
            sub=all_df[(all_df["tf"]==tf)&(all_df["filter_mode"]==mode)]
            v=sub[sub["valid"]==True] if "valid" in sub.columns else sub
            if len(v):
                b=v.iloc[0]; pg=b.get("pf_gain",0)
                print(f"  {tf} {mode:12s}: PF={b['oos_profit_factor']:.3f}"
                      f"  DD={b['oos_max_drawdown_pct']:.1f}%"
                      f"  trades={int(b['oos_trades'])}"
                      f"  gain={pg:+.3f}")

if __name__=="__main__":
    main()
