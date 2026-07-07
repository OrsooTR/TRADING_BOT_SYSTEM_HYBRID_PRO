"""
FFT Clock Trigger HFT Filter (#14) — Vectorized Backtest
EURUSD M1/M5/M15 | Train: 2020 | OOS: 2021-2025

Ipotesi (da SSRN-2487656):
  Quando lo spettro dei log-return mostra picchi persistenti sulle frequenze
  calendario (30min, 1h, 2h, 4h), il mercato è in regime "clock-driven":
  ordini meccanici TWAP/VWAP dominano, il rumore direzionale aumenta, e i
  segnali entry diventano meno affidabili.

Classificazione "clock-driven":
  1. clock_ratio = Σpower(clock_bins) / total_power > thresh_ratio
  2. persistence = frac(last P windows where clock bin è dominante) > thresh_pers

Test:
  A) Forward return stats per stato clock-driven/non (validazione)
  B) RSI filtrato: skip entry quando clock-driven
  C) Derivative filtrato: skip entry quando clock-driven
  D) Baseline time filter: skip prima barra di ogni ora (confronto non-FFT)
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
OUT_DIR = ROOT / "artifacts" / "clock_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "clock_backtests" / "reports"

# ── Grid ─────────────────────────────────────────────────────────────────────
FFT_NS         = {"M1":[64], "M5":[64,128], "M15":[64,128]}
RATIO_THRESHS  = [0.06, 0.08, 0.10]
PERS_THRESHS   = [0.30, 0.50]
PERS_WINDOWS   = [10, 20]
SESSIONS       = ["all", "london", "newyork", "asian"]
TIMEFRAMES     = ["M1", "M5", "M15"]

SESSION_H = {"all":(0,24),"london":(7,16),"newyork":(13,21),"asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK = 0.01
MAX_HOLD_TF = {"M1":100,"M5":300,"M15":200}

# Bars per hour per TF
BARS_PER_HOUR = {"M1":60, "M5":12, "M15":4}
# Clock periods to detect (in hours)
CLOCK_PERIODS_H = [0.5, 1.0, 2.0, 4.0]

PARAM_COLS = ["tf","strategy","fft_n","ratio_thresh","pers_thresh","pers_window",
              "session_label","filter_type"]

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

def calc_rsi(close,p=14,ob=70.0,os_=30.0):
    delta=np.diff(close,prepend=close[0])
    gain=np.where(delta>0,delta,0.0); loss=np.where(delta<0,-delta,0.0)
    ag=gain.copy(); al=loss.copy(); alpha=1.0/p
    for i in range(1,len(gain)):
        ag[i]=ag[i-1]*(1-alpha)+gain[i]*alpha
        al[i]=al[i-1]*(1-alpha)+loss[i]*alpha
    rs=np.where(al>0,ag/(al+1e-30),100.0)
    rsi=100.0-100.0/(1.0+rs)
    rsi_p=np.roll(rsi,1); rsi_p[0]=rsi[0]
    long_s  = (rsi>os_)&(rsi_p<=os_); long_s[0]=False
    short_s = (rsi<ob) &(rsi_p>=ob);  short_s[0]=False
    return long_s, short_s

def derivative_signals(close,ema_p=10):
    ema=calc_ema(close,ema_p)
    d1=np.diff(ema,prepend=ema[0])
    d1p=np.roll(d1,1); d1p[0]=d1[0]
    long_s  = (d1>0)&(d1p<=0); long_s[0]=False
    short_s = (d1<0)&(d1p>=0); short_s[0]=False
    return long_s, short_s

# ── Clock bins ────────────────────────────────────────────────────────────────
def get_clock_bins(tf: str, N: int) -> np.ndarray:
    """Bins DFT corrispondenti a periodi calendario per il TF dato."""
    bph = BARS_PER_HOUR[tf]
    n_bins = N // 2 + 1
    bins = []
    for ph in CLOCK_PERIODS_H:
        bars = bph * ph
        k = round(N / bars)
        if 1 <= k < n_bins:
            bins.append(k)
    return np.array(sorted(set(bins)), dtype=int)

# ── Clock-driven classifier ───────────────────────────────────────────────────
def compute_clock_signal(log_ret: np.ndarray, N: int, clock_bins: np.ndarray,
                          ratio_thresh: float, pers_thresh: float,
                          pers_window: int,
                          chunk_size: int = 300_000) -> np.ndarray:
    """
    Returns boolean array: True = clock-driven bar.
    clock_ratio  = power at clock bins / total power
    persistence  = frac of last pers_window windows where a clock bin was dominant
    clock-driven = (ratio > ratio_thresh) AND (persistence > pers_thresh)
    """
    T = len(log_ret)
    hann = np.hanning(N)
    n_bins = N // 2 + 1
    cb = clock_bins[clock_bins < n_bins]

    ratio_full   = np.zeros(T, dtype=np.float32)
    dom_bin_full = np.zeros(T, dtype=np.int32)

    def _chunk(wins):
        F    = np.fft.rfft(wins, axis=1)
        pwr  = np.abs(F)**2
        nb   = pwr.shape[1]
        tot  = pwr[:,1:].sum(axis=1) + 1e-30
        cb_  = cb[cb < nb]
        cr   = pwr[:,cb_].sum(axis=1) / tot if len(cb_) else np.zeros(len(wins))
        dom  = np.argmax(pwr[:,1:], axis=1) + 1
        return cr.astype(np.float32), dom.astype(np.int32)

    if T <= chunk_size + N:
        wins = sliding_window_view(log_ret, N) * hann
        cr, dom = _chunk(wins)
        ratio_full[N-1:]    = cr
        dom_bin_full[N-1:]  = dom
    else:
        step = chunk_size
        pos = 0
        while pos < T - N + 1:
            end = min(pos + step + N - 1, T)
            chunk = log_ret[pos:end]
            if len(chunk) < N: break
            wins = sliding_window_view(chunk, N) * hann
            cr, dom = _chunk(wins)
            out_idx = np.arange(pos+N-1, pos+N-1+len(cr))
            out_idx = out_idx[out_idx < T]
            n_out = len(out_idx)
            ratio_full[out_idx]   = cr[:n_out]
            dom_bin_full[out_idx] = dom[:n_out]
            pos += step

    # Persistence: sliding sum over pers_window using cumsum
    is_clock_dom = np.isin(dom_bin_full, cb).astype(np.float32)
    cum = np.cumsum(is_clock_dom)
    cum_shifted = np.roll(cum, pers_window); cum_shifted[:pers_window] = 0
    pers = (cum - cum_shifted) / pers_window

    clock_driven = (ratio_full > ratio_thresh) & (pers > pers_thresh)
    clock_driven[:N + pers_window] = False   # warmup

    return clock_driven

# ── Time-based (non-FFT) clock filter: first bar of each hour ─────────────────
def time_clock_mask(idx: pd.DatetimeIndex, tf: str) -> np.ndarray:
    """True = primo bar dell'ora (filtro calendare semplice senza FFT)."""
    if tf == "M1":
        return idx.minute == 0
    elif tf == "M5":
        return idx.minute == 0
    else:  # M15
        return idx.hour.values != np.roll(idx.hour.values, 1)

# ── Simulation ────────────────────────────────────────────────────────────────
def sim_and_metrics(eb, all_d, ep, sl_d, rr, high, low, max_hold):
    n=len(eb)
    if n==0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,
                "max_drawdown_pct":0.,"pnl_pct":0.,"longs":0,"shorts":0}
    N2=len(high); mj=min(max_hold,N2)
    rows=np.clip(eb[:,None]+np.arange(mj)[None,:],0,N2-1)
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
    eq=1.;peak=1.;mx_dd=0.
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

def apply_strategy(ls, ss, gate, sess_m, valid, op, atr, sl_mult, rr, high, low, mh):
    """gate=True → skip questo bar."""
    act = (~gate) & sess_m & valid
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
STRATS = {
    "rsi":        dict(sl_mult=1.5, rr=2.0, warmup=20),
    "derivative": dict(sl_mult=1.5, rr=3.0, warmup=15),
}

def run_grid(df, tf, clock_cache):
    close=df["close"].values; high=df["high"].values
    low=df["low"].values; op=df["open"].values
    idx=df.index; T=len(close)
    atr=calc_atr(df); mh=MAX_HOLD_TF[tf]
    lr=np.diff(np.log(close),prepend=np.log(close[0]))
    sm_cache={s:smask(idx,s) for s in SESSIONS}

    ls_rsi,  ss_rsi  = calc_rsi(close)
    ls_der,  ss_der  = derivative_signals(close)
    sig = {"rsi":(ls_rsi,ss_rsi), "derivative":(ls_der,ss_der)}

    # Time-based baseline gate (non-FFT)
    time_gate = time_clock_mask(idx, tf)

    results=[]
    no_gate=np.zeros(T, dtype=bool)   # nessun filtro = baseline

    for strat,sess in product(STRATS.keys(), SESSIONS):
        sp=STRATS[strat]; ls,ss=sig[strat]
        sm=sm_cache[sess]
        warmup=sp["warmup"]
        valid=np.zeros(T,dtype=bool); valid[warmup:]=True

        # BASELINE
        m=apply_strategy(ls,ss,no_gate,sm,valid,op,atr,sp["sl_mult"],sp["rr"],high,low,mh)
        results.append({"tf":tf,"strategy":strat,"fft_n":0,"ratio_thresh":0.,
                         "pers_thresh":0.,"pers_window":0,"session_label":sess,
                         "filter_type":"baseline",
                         "clock_pct":0., **m})

        # TIME-BASED filter
        m=apply_strategy(ls,ss,time_gate,sm,valid,op,atr,sp["sl_mult"],sp["rr"],high,low,mh)
        pct=float(time_gate.mean()*100)
        results.append({"tf":tf,"strategy":strat,"fft_n":0,"ratio_thresh":0.,
                         "pers_thresh":0.,"pers_window":0,"session_label":sess,
                         "filter_type":"time_clock",
                         "clock_pct":pct, **m})

        # FFT CLOCK filter
        for N,rt,pt,pw in product(FFT_NS[tf],RATIO_THRESHS,PERS_THRESHS,PERS_WINDOWS):
            key=(N,rt,pt,pw)
            if key not in clock_cache:
                cb=get_clock_bins(tf,N)
                clock_cache[key]=compute_clock_signal(lr,N,cb,rt,pt,pw)
            gate=clock_cache[key]
            w2=max(warmup,N+pw)
            valid2=np.zeros(T,dtype=bool); valid2[w2:]=True
            m=apply_strategy(ls,ss,gate,sm,valid2,op,atr,sp["sl_mult"],sp["rr"],high,low,mh)
            pct=float(gate.mean()*100)
            results.append({"tf":tf,"strategy":strat,"fft_n":N,"ratio_thresh":rt,
                             "pers_thresh":pt,"pers_window":pw,"session_label":sess,
                             "filter_type":"fft_clock",
                             "clock_pct":pct, **m})
    return results

# ── Test A: forward return stats ──────────────────────────────────────────────
def test_a(df, tf):
    close=df["close"].values; T=len(close)
    lr=np.diff(np.log(close),prepend=np.log(close[0]))
    fwd10=np.zeros(T)
    for i in range(T-10): fwd10[i]=lr[i+1:i+11].sum()
    records=[]
    for N,rt,pt,pw in product(FFT_NS[tf],RATIO_THRESHS[:2],PERS_THRESHS,PERS_WINDOWS[:1]):
        cb=get_clock_bins(tf,N)
        gate=compute_clock_signal(lr,N,cb,rt,pt,pw)
        for label,mask in [("clock_driven",gate),("non_clock",~gate&(np.cumsum(gate)>0))]:
            n=int(mask.sum())
            if n<50: continue
            records.append({"tf":tf,"fft_n":N,"ratio_thresh":rt,"pers_thresh":pt,
                             "pers_window":pw,"state":label,
                             "avg_return_pip":round(np.nanmean(fwd10[mask])*10000,3),
                             "std_pip":round(np.nanstd(fwd10[mask])*10000,3),
                             "n_bars":n, "pct":round(n/T*100,1)})
    return pd.DataFrame(records)

# ── Combine ───────────────────────────────────────────────────────────────────
def build_combined(tf, tr_list, os_list):
    key_cols=["tf","strategy","fft_n","ratio_thresh","pers_thresh","pers_window",
              "session_label","filter_type"]
    metric_cols=["trades","win_rate","profit_factor","max_drawdown_pct","pnl_pct","longs","shorts"]
    def pfx(rows,p):
        df=pd.DataFrame(rows)
        return df.rename(columns={c:f"{p}_{c}" for c in metric_cols if c in df.columns})
    tr=pfx(tr_list,"train"); os=pfx(os_list,"oos")
    merge_on=[c for c in key_cols if c in tr.columns and c in os.columns]
    os_drop=[c for c in os.columns if c not in merge_on and not c.startswith("oos_")
             and c in tr.columns and not c.startswith("train_")]
    m=tr.merge(os.drop(columns=os_drop,errors="ignore"),on=merge_on,how="inner")
    if "oos_profit_factor" in m.columns and "train_profit_factor" in m.columns:
        m["delta_pf"]=round(m["oos_profit_factor"]-m["train_profit_factor"],4)
    # PF gain vs baseline per (strat, session)
    base_key=["tf","strategy","session_label"]
    base=m[m.filter_type=="baseline"][base_key+["oos_profit_factor","oos_max_drawdown_pct","oos_trades"]]
    base=base.rename(columns={"oos_profit_factor":"base_pf",
                               "oos_max_drawdown_pct":"base_dd","oos_trades":"base_trades"})
    m=m.merge(base,on=base_key,how="left")
    m["pf_gain"]=round(m["oos_profit_factor"]-m["base_pf"],4)
    return m.sort_values(["pf_gain","oos_profit_factor","oos_max_drawdown_pct"],
                         ascending=[False,False,True]).reset_index(drop=True)

# ── Report ────────────────────────────────────────────────────────────────────
def write_report(label, df, ts):
    RPT_DIR.mkdir(parents=True, exist_ok=True)
    filt=df[df.filter_type!="baseline"].reset_index(drop=True)
    if not len(filt): return
    b=filt.iloc[0]
    lines=[f"# FFT Clock Trigger HFT Filter (#14) — {label}","",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_clock_trigger_hft_filter]]","",
        f"- Generated: {ts}  |  Combos: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025","",
        "## Logica",
        "- Rolling FFT (Hann) su log-return → clock_ratio = potenza su bin calendario",
        "- Persistence = frac finestre dove bin clock è dominante",
        "- Gate: clock_driven = (ratio > thresh) AND (pers > thresh) → skip entry",
        "- Confronto: FFT clock filter vs time-based (prima barra di ogni ora)","",
        f"## Best setup",
        f"- {b['strategy'].upper()} | filter={b['filter_type']}",
        f"- N={int(b['fft_n'])} ratio>{b['ratio_thresh']:.2f} pers>{b['pers_thresh']:.2f} P={int(b['pers_window'])}",
        f"- Session={b['session_label']} | OOS PF={b['oos_profit_factor']:.3f}",
        f"- PF Gain={b['pf_gain']:+.3f} | OOS DD={b['oos_max_drawdown_pct']:.1f}% | Trades={int(b['oos_trades'])}","",
        "## Top 10","",
        "| # | Strat | Filter | N | Ratio | Pers | P | Sess | Train PF | OOS PF | OOS DD% | PF Gain | Clock% |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i,r in enumerate(filt.head(10).itertuples(index=False),1):
        d=r._asdict()
        lines.append(
            f"| {i} | {d['strategy']} | {d['filter_type'][:8]} | {int(d['fft_n'])}"
            f" | {d['ratio_thresh']:.2f} | {d['pers_thresh']:.2f} | {int(d['pers_window'])}"
            f" | {d['session_label']} | {d['train_profit_factor']:.3f}"
            f" | {d['oos_profit_factor']:.3f} | {d['oos_max_drawdown_pct']:.1f}"
            f" | {d.get('pf_gain',0):+.3f} | {d.get('clock_pct',0):.1f}% |")
    (RPT_DIR/f"clock_report_{label.lower()}.md").write_text("\n".join(lines)+"\n",encoding="utf-8")

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ts=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("Loading M1..."); t0=time.time()
    m1=load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")
    all_dfs=[]; all_ta=[]

    for tf in TIMEFRAMES:
        print(f"\n[{tf}] resampling...")
        tf_df=resample(m1,tf)
        train=tf_df.loc[TRAIN_S:TRAIN_E]; oos=tf_df.loc[OOS_S:OOS_E]
        n_fft=len(FFT_NS[tf])*len(RATIO_THRESHS)*len(PERS_THRESHS)*len(PERS_WINDOWS)
        nc=(1+1+n_fft)*len(STRATS)*len(SESSIONS)*2
        print(f"  train={len(train)} oos={len(oos)} combos≈{nc}")
        t1=time.time()
        # Test A
        ta=pd.concat([test_a(train,tf).assign(split="train"),
                       test_a(oos,tf).assign(split="oos")])
        all_ta.append(ta)
        # Grid
        cc_tr={}; cc_os={}
        tr_rows=run_grid(train,tf,cc_tr)
        os_rows=run_grid(oos,tf,cc_os)
        combined=build_combined(tf,tr_rows,os_rows)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR/f"clock_results_{tf.lower()}.csv",index=False)
        filt=combined[combined.filter_type!="baseline"]
        if len(filt):
            b=filt.iloc[0]
            print(f"  {time.time()-t1:.1f}s | best: {b['strategy']} {b['filter_type'][:8]}"
                  f" PF={b['oos_profit_factor']:.3f} gain={b.get('pf_gain',0):+.3f}"
                  f" clock%={b.get('clock_pct',0):.1f}%")

    ta_df=pd.concat(all_ta)
    ta_df.to_csv(OUT_DIR/"clock_test_a.csv",index=False)
    all_df=pd.concat(all_dfs).sort_values(["pf_gain","oos_profit_factor","oos_max_drawdown_pct"],
                                           ascending=[False,False,True]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR/"clock_results_all.csv",index=False)
    all_df.to_json(OUT_DIR/"clock_results_all.json",orient="records",indent=2)
    write_report("ALL_TFS",all_df,ts)
    for tf in TIMEFRAMES:
        sub=all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf,sub,ts)

    print(f"\nDone. {len(all_df)} rows.")
    print("\n=== SUMMARY ===")
    for strat in ["rsi","derivative"]:
        for tf in TIMEFRAMES:
            sub=all_df[(all_df.strategy==strat)&(all_df.tf==tf)]
            base=sub[sub.filter_type=="baseline"]
            filt=sub[(sub.filter_type=="fft_clock")]
            time_f=sub[sub.filter_type=="time_clock"]
            if len(base) and len(filt):
                bpf=base.iloc[0].oos_profit_factor
                fpf=filt.iloc[0].oos_profit_factor
                tpf=time_f.iloc[0].oos_profit_factor if len(time_f) else 0
                print(f"  {strat:12s} {tf}: base={bpf:.3f}  "
                      f"time_clock={tpf:.3f}(+{tpf-bpf:+.3f})  "
                      f"fft_clock={fpf:.3f}({filt.iloc[0].get('pf_gain',0):+.3f})")

if __name__=="__main__":
    main()
