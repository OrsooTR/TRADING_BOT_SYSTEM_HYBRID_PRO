"""
EMA Ribbon Direction Filter — Vectorized Backtester
EURUSD M1/M5/M15 | 2020-2025  |  Train: 2020  |  OOS: 2021-2025
Signal: ribbon JUST flipped fully bullish/bearish (fast>mid>slow or reverse)
"""
from __future__ import annotations
import numpy as np, pandas as pd, json, os, time
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parent.parent
HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", ROOT / "data" / "histdata"))
ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
        for y in [2020,2021,2022,2023,2024,2025]]
OUT_DIR = ROOT / "artifacts" / "ribbon_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "ribbon_backtests" / "reports"

# Grid
FAST_EMAS  = [5, 8, 13]
MID_EMAS   = [21, 34]
SLOW_EMAS  = [55, 89]
SL_MULTS   = [1.0, 1.5]
RRS        = [2.0, 3.0, 4.0]
SESSIONS   = ["all", "london", "newyork", "asian"]
TIMEFRAMES = ["M1", "M5", "M15"]
# valid combos: 3×2×2 fast/mid/slow (fast<mid<slow always) × 2 sl × 3 rr × 4 sess = 288

SESSION_H  = {"all":(0,24),"london":(7,16),"newyork":(13,21),"asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK = 0.01
MAX_HOLD_PER_TF = {"M1":100, "M5":300, "M15":200}
PARAM_COLS = ["fast_ema","mid_ema","slow_ema","sl_atr_mult","rr","session_label"]

# ── data ──────────────────────────────────────────────────────────────────────
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

# ── indicators ─────────────────────────────────────────────────────────────────
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

def smask(idx,sess):
    # HistData usa timestamp EST (GMT-5, no DST): shift a UTC prima delle sessioni
    h=(idx.hour+5)%24; s,e=SESSION_H[sess]
    return (h>=s) if e==24 else (h>=s)&(h<e)

# ── simulation (same as ATR script) ────────────────────────────────────────────
def sim_and_metrics(entry_bars,directions,ep,sl_d,rr,high,low,max_hold=200):
    n=len(entry_bars)
    if n==0:
        return {"trades":0,"win_rate":0.,"profit_factor":0.,"max_drawdown_pct":0.,
                "pnl_pct":0.,"longs":0,"shorts":0,"avg_bars":0.}
    N=len(high); mj=min(max_hold,N)
    rows=np.clip(entry_bars[:,None]+np.arange(mj)[None,:],0,N-1)
    H=high[rows]; L=low[rows]
    tp_p=ep+directions*rr*sl_d; sl_p=ep-directions*sl_d
    li=directions==1; si=directions==-1
    tp_hit=np.zeros((n,mj),dtype=bool); sl_hit=np.zeros((n,mj),dtype=bool)
    if li.any():
        tp_hit[li]=H[li]>=tp_p[li,None]; sl_hit[li]=L[li]<=sl_p[li,None]
    if si.any():
        tp_hit[si]=L[si]<=tp_p[si,None]; sl_hit[si]=H[si]>=sl_p[si,None]
    tp_b=np.where(tp_hit.any(1),np.argmax(tp_hit,1),mj)
    sl_b=np.where(sl_hit.any(1),np.argmax(sl_hit,1),mj)
    # tie-break pessimistico: se TP e SL cadono nella stessa barra conta lo SL
    win=(tp_b<sl_b)&(tp_b<mj); lose=(sl_b<=tp_b)&(sl_b<mj)
    pnl_r=np.where(win,rr,np.where(lose,-1.,0.))
    exit_b=np.where(win,tp_b,np.where(lose,sl_b,mj))
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
            "pnl_pct":round((eq-1)*100,2),"longs":int(li.sum()),
            "shorts":int(si.sum()),"avg_bars":round(float(exit_b.mean()),1)}

# ── EMA Ribbon grid ─────────────────────────────────────────────────────────────
def run_ribbon_grid(df, max_hold=200):
    close=df["close"].values; high=df["high"].values
    low=df["low"].values;     op=df["open"].values
    idx=df.index; atr=calc_atr(df); N=len(close)

    # precompute all unique EMA periods
    all_periods=set(FAST_EMAS+MID_EMAS+SLOW_EMAS)
    ema_cache={p:calc_ema(close,p) for p in all_periods}
    sm_cache={s:smask(idx,s) for s in SESSIONS}

    results=[]
    for fp,mp,sp,sl_m,rr,sess in product(FAST_EMAS,MID_EMAS,SLOW_EMAS,SL_MULTS,RRS,SESSIONS):
        if not (fp < mp < sp): continue   # skip invalid ribbon combos

        ef=ema_cache[fp]; em=ema_cache[mp]; es=ema_cache[sp]
        sm=sm_cache[sess]
        warmup=max(fp,mp,sp)+2
        valid=np.zeros(N,dtype=bool); valid[warmup:]=True
        act=sm&valid

        # ribbon state at current and previous bar
        bull_now  = (ef>em) & (em>es)
        bear_now  = (ef<em) & (em<es)
        bull_prev = np.roll(bull_now,1); bull_prev[0]=False
        bear_prev = np.roll(bear_now,1); bear_prev[0]=False

        # long: ribbon JUST turned fully bullish
        l_sig = act & bull_now & ~bull_prev; l_sig[0]=False
        # short: ribbon JUST turned fully bearish
        s_sig = act & bear_now & ~bear_prev; s_sig[0]=False

        li=np.where(l_sig)[0]; si=np.where(s_sig)[0]
        all_i=np.concatenate([li,si])
        all_d=np.concatenate([np.ones(len(li)),-np.ones(len(si))])

        if len(all_i)==0:
            results.append({**dict(zip(PARAM_COLS,[fp,mp,sp,sl_m,rr,sess])),
                "trades":0,"win_rate":0.,"profit_factor":0.,"max_drawdown_pct":0.,
                "pnl_pct":0.,"longs":0,"shorts":0,"avg_bars":0.}); continue

        order=np.argsort(all_i,kind="stable")
        all_i=all_i[order]; all_d=all_d[order]
        eb=np.minimum(all_i+1,N-1)
        ep=op[eb]; sl_d=sl_m*atr[all_i]
        m=sim_and_metrics(eb,all_d,ep,sl_d,rr,high,low,max_hold)
        results.append({**dict(zip(PARAM_COLS,[fp,mp,sp,sl_m,rr,sess])),**m})
    return results

# ── combine & sort ─────────────────────────────────────────────────────────────
def build_combined(tf,tr,os):
    def pfx(df,p): return df.rename(columns={c:f"{p}_{c}" for c in
        ["trades","win_rate","profit_factor","max_drawdown_pct","pnl_pct","longs","shorts","avg_bars"]})
    m=pfx(pd.DataFrame(tr),"train").merge(pfx(pd.DataFrame(os),"oos"),on=PARAM_COLS,how="inner")
    m.insert(0,"tf",tf)
    m["total_trades"]=m["train_trades"]+m["oos_trades"]
    m["total_longs"]=m["train_longs"]+m["oos_longs"]
    m["total_shorts"]=m["train_shorts"]+m["oos_shorts"]
    def wa(r):
        wt,wo=r["train_trades"],r["oos_trades"]
        return (r["train_avg_bars"]*wt+r["oos_avg_bars"]*wo)/(wt+wo) if (wt+wo)>0 else 0.
    m["avg_bars"]=m.apply(wa,axis=1)
    m=m.drop(columns=["train_longs","train_shorts","train_avg_bars",
                        "oos_longs","oos_shorts","oos_avg_bars"])
    return m.sort_values(["oos_profit_factor","oos_max_drawdown_pct","oos_pnl_pct"],
                         ascending=[False,True,False]).reset_index(drop=True)

# ── report ──────────────────────────────────────────────────────────────────────
def write_report(label,df,ts):
    RPT_DIR.mkdir(parents=True,exist_ok=True)
    b=df.iloc[0]
    ncombos_valid=len(FAST_EMAS)*len(MID_EMAS)*len(SLOW_EMAS)  # = 12 ribbon combos
    lines=[f"# EMA Ribbon Direction Filter — EURUSD {label}","",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/INDEX]]","",
        f"- Generated: {ts}  |  Combinations: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025","",
        "## Logic",
        "- Ribbon: EMA(fast) / EMA(mid) / EMA(slow)  — condizione: fast < mid < slow",
        "- Long:  ribbon JUST turned fully bullish  (fast>mid>slow, bar prec. NO)",
        "- Short: ribbon JUST turned fully bearish  (fast<mid<slow, bar prec. NO)",
        "- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr",
        "- Session filter on signal bar","",
        "## Best Setup",
        f"- TF={b['tf']}  fast={int(b['fast_ema'])}  mid={int(b['mid_ema'])}  slow={int(b['slow_ema'])}",
        f"- SL_mult={b['sl_atr_mult']:.1f}  RR={b['rr']:.1f}  Session={b['session_label']}",
        f"- Train PF={b['train_profit_factor']:.4f}  |  OOS PF={b['oos_profit_factor']:.4f}",
        f"- OOS DD={b['oos_max_drawdown_pct']:.2f}%  |  OOS P&L={b['oos_pnl_pct']:.2f}%","",
        "## Top 10","",
        "| # | TF | Fast | Mid | Slow | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i,r in enumerate(df.head(10).itertuples(index=False),1):
        d=r._asdict()
        lines.append(f"| {i} | {d['tf']} | {int(d['fast_ema'])} | {int(d['mid_ema'])} | {int(d['slow_ema'])}"
            f" | {d['sl_atr_mult']:.1f} | {d['rr']:.1f} | {d['session_label']}"
            f" | {d['train_profit_factor']:.3f} | {d['oos_profit_factor']:.3f}"
            f" | {d['oos_max_drawdown_pct']:.2f} | {d['oos_pnl_pct']:.2f} |")
    (RPT_DIR/f"ribbon_report_{label.lower().replace(' ','_')}.md"
     ).write_text("\n".join(lines)+"\n",encoding="utf-8")

# ── main ───────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    ts=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("Loading M1 data..."); t0=time.time()
    m1=load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")
    valid_ribbon=sum(1 for fp,mp,sp in product(FAST_EMAS,MID_EMAS,SLOW_EMAS) if fp<mp<sp)
    ncombos=valid_ribbon*len(SL_MULTS)*len(RRS)*len(SESSIONS)
    all_dfs=[]
    for tf in TIMEFRAMES:
        print(f"\n[{tf}] resampling...")
        tf_df=resample(m1,tf)
        train=tf_df.loc[TRAIN_S:TRAIN_E]; oos=tf_df.loc[OOS_S:OOS_E]
        print(f"  train={len(train)}  oos={len(oos)}  combos={ncombos}")
        t1=time.time()
        mh=MAX_HOLD_PER_TF[tf]
        tr=run_ribbon_grid(train,mh); os_=run_ribbon_grid(oos,mh)
        combined=build_combined(tf,tr,os_)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR/f"ribbon_results_{tf.lower()}.csv",index=False)
        b=combined.iloc[0]
        print(f"  {time.time()-t1:.1f}s | best OOS: PF={b['oos_profit_factor']:.3f}"
              f" DD={b['oos_max_drawdown_pct']:.1f}% P&L={b['oos_pnl_pct']:.1f}%")
    all_df=pd.concat(all_dfs).sort_values(
        ["oos_profit_factor","oos_max_drawdown_pct","oos_pnl_pct"],
        ascending=[False,True,False]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR/"ribbon_results_all.csv",index=False)
    all_df.to_json(OUT_DIR/"ribbon_results_all.json",orient="records",indent=2)
    write_report("ALL_TFS",all_df,ts)
    for tf in TIMEFRAMES:
        sub=all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf,sub,ts)
    print(f"\nRibbon done. {len(all_df)} total rows.")

if __name__=="__main__":
    main()
