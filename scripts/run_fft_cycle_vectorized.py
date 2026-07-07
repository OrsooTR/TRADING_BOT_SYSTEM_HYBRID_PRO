"""
FFT Dominant Cycle (#11) — Vectorized Backtester
EURUSD M1/M5/M15 | Train: 2020 | OOS: 2021-2025
Sessions: all | london | newyork | asian

Signal:
  1. Rolling FFT on log-returns with Hann window
  2. Find dominant bin in mid-band (skip low=trend and high=noise)
  3. Reconstruct signal via IFFT single bin
  4. Long  when slope JUST turns positive (zero-crossing up)   + quality filter
  5. Short when slope JUST turns negative (zero-crossing down) + quality filter
  Quality filter: dominant cycle SNR > min_snr AND dom_period > min_period bars
"""
from __future__ import annotations
import numpy as np, pandas as pd, json, os, time
from pathlib import Path
from zipfile import ZipFile
from itertools import product
from numpy.lib.stride_tricks import sliding_window_view
from datetime import datetime, UTC

ROOT = Path(__file__).resolve().parent.parent
HISTDATA_DIR = Path(os.environ.get("HISTDATA_DIR", ROOT / "data" / "histdata"))
ZIPS = [HISTDATA_DIR / f"HISTDATA_COM_ASCII_EURUSD_M1{y}.zip"
        for y in [2020,2021,2022,2023,2024,2025]]
OUT_DIR = ROOT / "artifacts" / "fft_cycle_backtests" / "data"
RPT_DIR = ROOT / "artifacts" / "fft_cycle_backtests" / "reports"

# Grid
FFT_WINDOWS    = {"M1":[64], "M5":[64,128], "M15":[64,128,256]}
LOW_PCTS       = [0.05, 0.10]   # fraction of low-freq bins to exclude (trend)
HIGH_PCTS      = [0.20, 0.30]   # fraction of high-freq bins to exclude (noise)
MIN_PERIODS    = [5, 10]        # minimum dominant cycle length in bars
SL_MULTS       = [1.0, 1.5]
RRS            = [2.0, 3.0, 4.0]
SESSIONS       = ["all", "london", "newyork", "asian"]
MIN_SNR        = 1.5            # fixed quality gate (SNR of dominant bin vs band mean)

SESSION_H = {"all":(0,24), "london":(7,16), "newyork":(13,21), "asian":(0,8)}
TRAIN_S, TRAIN_E = "2020-01-01", "2020-12-31 23:59:59"
OOS_S,   OOS_E   = "2021-01-01", "2025-12-31 23:59:59"
RISK        = 0.01
MAX_HOLD_TF = {"M1":100, "M5":300, "M15":200}
PARAM_COLS  = ["fft_window","low_pct","high_pct","min_period","sl_atr_mult","rr","session_label"]

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

def smask(idx,sess):
    # HistData usa timestamp EST (GMT-5, no DST): shift a UTC prima delle sessioni
    h=(idx.hour+5)%24; s,e=SESSION_H[sess]
    return (h>=s) if e==24 else (h>=s)&(h<e)

# ── FFT signal computation ─────────────────────────────────────────────────────
def compute_fft_signals_chunked(log_ret: np.ndarray, N: int,
                                 low_pct: float, high_pct: float,
                                 chunk_size: int = 200_000) -> tuple:
    """Chunked version for large arrays (M1) to avoid OOM."""
    T = len(log_ret)
    hann = np.hanning(N)
    n_bins_expected = N // 2 + 1

    slope_arr   = np.full(T, np.nan)
    snr_full    = np.zeros(T)
    period_full = np.zeros(T)

    low_bin  = max(1, int(n_bins_expected * low_pct))
    high_bin = max(low_bin+1, int(n_bins_expected * (1.0 - high_pct)))
    mask = np.zeros(n_bins_expected, dtype=bool)
    mask[low_bin:high_bin] = True
    band_n = mask.sum()

    # Process with overlap = N-1 so we don't miss windows at chunk boundaries
    step = chunk_size
    start = 0
    while start < T - N + 1:
        end = min(start + step + N - 1, T)
        chunk = log_ret[start:end]
        if len(chunk) < N:
            break
        wins   = sliding_window_view(chunk, N) * hann
        F      = np.fft.rfft(wins, axis=1)
        power  = np.abs(F)**2
        pwr_m  = power * mask[None, :]
        dom_bin= np.argmax(pwr_m, axis=1)
        rows   = np.arange(len(dom_bin))
        dom_pw = power[rows, dom_bin]
        bnd_pw = pwr_m.sum(axis=1)
        snr    = dom_pw / (bnd_pw / max(band_n,1) + 1e-30)
        dper   = N / (dom_bin.astype(float) + 1e-9)
        F_filt = np.zeros_like(F)
        F_filt[rows, dom_bin] = F[rows, dom_bin]
        recon  = np.fft.irfft(F_filt, n=N, axis=1)[:, -1]

        # Map back: window i covers log_ret[start+i : start+i+N], last sample = start+i+N-1
        out_indices = np.arange(start + N - 1, start + N - 1 + len(recon))
        out_indices = out_indices[out_indices < T]
        n_out = len(out_indices)
        slope_arr[out_indices]   = recon[:n_out]
        snr_full[out_indices]    = snr[:n_out]
        period_full[out_indices] = dper[:n_out]

        start += step
        del wins, F, power, pwr_m, F_filt

    slope_full = np.diff(slope_arr, prepend=np.nan)
    return slope_full, snr_full, period_full


def compute_fft_signals(log_ret: np.ndarray, N: int,
                         low_pct: float, high_pct: float) -> tuple:
    """
    Returns (slope_full, snr_full, period_full) — all length T, NaN for first N-1 bars.
    slope_full : derivative of the dominant-cycle reconstruction
    snr_full   : SNR of dominant bin vs mean in-band power
    period_full: dominant cycle period in bars
    """
    T = len(log_ret)
    hann = np.hanning(N)

    wins = sliding_window_view(log_ret, N) * hann           # (T-N+1, N)
    F    = np.fft.rfft(wins, axis=1)                        # (T-N+1, n_bins)
    power= np.abs(F)**2                                     # (T-N+1, n_bins)

    n_bins   = F.shape[1]
    low_bin  = max(1, int(n_bins * low_pct))
    high_bin = max(low_bin+1, int(n_bins * (1.0 - high_pct)))

    mask = np.zeros(n_bins, dtype=bool)
    mask[low_bin:high_bin] = True
    band_n = mask.sum()

    pwr_masked  = power * mask[None, :]
    dom_bin     = np.argmax(pwr_masked, axis=1)             # (T-N+1,)

    rows        = np.arange(len(dom_bin))
    dom_power   = power[rows, dom_bin]
    band_power  = pwr_masked.sum(axis=1)
    snr         = dom_power / (band_power / max(band_n, 1) + 1e-30)
    dom_period  = N / (dom_bin.astype(float) + 1e-9)

    # Reconstruct last sample of dominant bin via IFFT
    F_filt          = np.zeros_like(F)
    F_filt[rows, dom_bin] = F[rows, dom_bin]
    recon           = np.fft.irfft(F_filt, n=N, axis=1)[:, -1]  # (T-N+1,)

    # Align to full T-length arrays
    slope_arr  = np.full(T, np.nan)
    slope_arr[N-1:] = recon
    slope_full = np.diff(slope_arr, prepend=np.nan)          # first difference = slope

    snr_full    = np.zeros(T); snr_full[N-1:]    = snr
    period_full = np.zeros(T); period_full[N-1:] = dom_period

    return slope_full, snr_full, period_full

# ── simulation (identical to previous scripts) ────────────────────────────────
def sim_and_metrics(entry_bars, directions, ep, sl_d, rr, high, low, max_hold=200):
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

# ── grid runner ────────────────────────────────────────────────────────────────
def run_fft_grid(df: pd.DataFrame, tf: str) -> list[dict]:
    close=df["close"].values; high=df["high"].values
    low=df["low"].values;     op=df["open"].values
    idx=df.index; atr=calc_atr(df); N_bars=len(close)
    log_ret=np.diff(np.log(close), prepend=np.log(close[0]))
    max_hold=MAX_HOLD_TF[tf]
    sm_cache={s:smask(idx,s) for s in SESSIONS}
    windows=FFT_WINDOWS[tf]
    results=[]

    # Cache FFT signals per (N, low_pct, high_pct) to avoid recomputation
    fft_cache: dict = {}
    for N,lp,hp in product(windows, LOW_PCTS, HIGH_PCTS):
        key=(N,lp,hp)
        if key not in fft_cache:
            if tf == "M1":
                fft_cache[key] = compute_fft_signals_chunked(log_ret, N, lp, hp)
            else:
                fft_cache[key] = compute_fft_signals(log_ret, N, lp, hp)

    for N,lp,hp,min_p,sl_m,rr,sess in product(
            windows, LOW_PCTS, HIGH_PCTS, MIN_PERIODS, SL_MULTS, RRS, SESSIONS):

        slope_full, snr_full, period_full = fft_cache[(N,lp,hp)]
        sm  = sm_cache[sess]
        warmup = N + 2
        valid = np.zeros(N_bars, dtype=bool); valid[warmup:] = True
        quality = (snr_full >= MIN_SNR) & (period_full >= min_p)
        act = sm & valid & quality

        slope_prev = np.roll(slope_full, 1)
        l_sig = act & (slope_full > 0) & (slope_prev <= 0)
        s_sig = act & (slope_full < 0) & (slope_prev >= 0)
        l_sig[0]=False; s_sig[0]=False

        li=np.where(l_sig)[0]; si=np.where(s_sig)[0]
        all_i=np.concatenate([li,si])
        all_d=np.concatenate([np.ones(len(li)),-np.ones(len(si))])

        if len(all_i)==0:
            results.append({**dict(zip(PARAM_COLS,[N,lp,hp,min_p,sl_m,rr,sess])),
                "trades":0,"win_rate":0.,"profit_factor":0.,"max_drawdown_pct":0.,
                "pnl_pct":0.,"longs":0,"shorts":0,"avg_bars":0.}); continue

        order=np.argsort(all_i,kind="stable")
        all_i=all_i[order]; all_d=all_d[order]
        eb=np.minimum(all_i+1, N_bars-1)
        ep=op[eb]; sl_d=sl_m*atr[all_i]
        m=sim_and_metrics(eb,all_d,ep,sl_d,rr,high,low,max_hold)
        results.append({**dict(zip(PARAM_COLS,[N,lp,hp,min_p,sl_m,rr,sess])),**m})

    return results

# ── combine & sort ─────────────────────────────────────────────────────────────
def build_combined(tf, tr, os_):
    def pfx(df,p): return df.rename(columns={c:f"{p}_{c}" for c in
        ["trades","win_rate","profit_factor","max_drawdown_pct","pnl_pct","longs","shorts","avg_bars"]})
    m=pfx(pd.DataFrame(tr),"train").merge(pfx(pd.DataFrame(os_),"oos"),on=PARAM_COLS,how="inner")
    m.insert(0,"tf",tf)
    m["total_trades"] =m["train_trades"] +m["oos_trades"]
    m["total_longs"]  =m["train_longs"]  +m["oos_longs"]
    m["total_shorts"] =m["train_shorts"] +m["oos_shorts"]
    def wa(r):
        wt,wo=r["train_trades"],r["oos_trades"]
        return (r["train_avg_bars"]*wt+r["oos_avg_bars"]*wo)/(wt+wo) if (wt+wo)>0 else 0.
    m["avg_bars"]=m.apply(wa,axis=1)
    m=m.drop(columns=["train_longs","train_shorts","train_avg_bars",
                        "oos_longs","oos_shorts","oos_avg_bars"])
    return m.sort_values(["oos_profit_factor","oos_max_drawdown_pct","oos_pnl_pct"],
                         ascending=[False,True,False]).reset_index(drop=True)

# ── report ──────────────────────────────────────────────────────────────────────
def write_report(label, df, ts):
    RPT_DIR.mkdir(parents=True,exist_ok=True)
    b=df.iloc[0]
    lines=[f"# FFT Dominant Cycle (#11) — EURUSD {label}","",
        "- [[../../../Pipeline_01/04_BACKTEST/INDEX]]",
        "- [[../../../Pipeline_01/03_STRATEGIES/IDEAS/fft_dominant_cycle]]","",
        f"- Generated: {ts}  |  Combinations: {len(df)}",
        "- Train: 2020  |  OOS: 2021-2025","",
        "## Logic",
        "- Rolling FFT on log-returns with Hann window (size N)",
        "- Mid-band mask: exclude low_pct (trend) and high_pct (noise) bins",
        "- Dominant bin = max energy in mid-band",
        "- Quality filter: SNR > 1.5 AND dominant period > min_period bars",
        "- Long:  cycle slope JUST turned positive (zero-crossing up)",
        "- Short: cycle slope JUST turned negative (zero-crossing down)",
        "- Entry: next-bar open  |  SL: ±sl_mult×ATR(14)  |  TP: SL×rr","",
        "## Best Setup",
        f"- TF={b['tf']}  N={int(b['fft_window'])}  low_pct={b['low_pct']:.2f}  high_pct={b['high_pct']:.2f}",
        f"- min_period={int(b['min_period'])}b  SL_mult={b['sl_atr_mult']:.1f}  RR={b['rr']:.1f}  Session={b['session_label']}",
        f"- Train PF={b['train_profit_factor']:.4f}  |  OOS PF={b['oos_profit_factor']:.4f}",
        f"- OOS DD={b['oos_max_drawdown_pct']:.2f}%  |  OOS P&L={b['oos_pnl_pct']:.2f}%","",
        "## Top 10","",
        "| # | TF | N | low% | high% | min_p | SL | RR | Session | Train PF | OOS PF | OOS DD% | OOS P&L% |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i,r in enumerate(df.head(10).itertuples(index=False),1):
        d=r._asdict()
        lines.append(
            f"| {i} | {d['tf']} | {int(d['fft_window'])} | {d['low_pct']:.2f} | {d['high_pct']:.2f}"
            f" | {int(d['min_period'])} | {d['sl_atr_mult']:.1f} | {d['rr']:.1f} | {d['session_label']}"
            f" | {d['train_profit_factor']:.3f} | {d['oos_profit_factor']:.3f}"
            f" | {d['oos_max_drawdown_pct']:.2f} | {d['oos_pnl_pct']:.2f} |")
    (RPT_DIR/f"fft_cycle_report_{label.lower().replace(' ','_')}.md"
     ).write_text("\n".join(lines)+"\n",encoding="utf-8")

# ── main ───────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True,exist_ok=True)
    ts=datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("Loading M1 data..."); t0=time.time()
    m1=load_m1(ZIPS)
    print(f"  {len(m1)} bars in {time.time()-t0:.1f}s")

    all_dfs=[]
    for tf in ["M1","M5","M15"]:
        print(f"\n[{tf}] resampling...")
        tf_df=resample(m1,tf)
        train=tf_df.loc[TRAIN_S:TRAIN_E]; oos=tf_df.loc[OOS_S:OOS_E]
        nw=len(FFT_WINDOWS[tf])
        ncombos=nw*len(LOW_PCTS)*len(HIGH_PCTS)*len(MIN_PERIODS)*len(SL_MULTS)*len(RRS)*len(SESSIONS)
        print(f"  train={len(train)} bars  oos={len(oos)} bars  combos={ncombos}")
        t1=time.time()
        tr=run_fft_grid(train,tf); os_=run_fft_grid(oos,tf)
        elapsed=time.time()-t1
        combined=build_combined(tf,tr,os_)
        all_dfs.append(combined)
        combined.to_csv(OUT_DIR/f"fft_cycle_results_{tf.lower()}.csv",index=False)
        b=combined.iloc[0]
        print(f"  {elapsed:.1f}s | best OOS: PF={b['oos_profit_factor']:.3f}"
              f" DD={b['oos_max_drawdown_pct']:.1f}% P&L={b['oos_pnl_pct']:.1f}%")

    all_df=pd.concat(all_dfs).sort_values(
        ["oos_profit_factor","oos_max_drawdown_pct","oos_pnl_pct"],
        ascending=[False,True,False]).reset_index(drop=True)
    all_df.to_csv(OUT_DIR/"fft_cycle_results_all.csv",index=False)
    all_df.to_json(OUT_DIR/"fft_cycle_results_all.json",orient="records",indent=2)
    write_report("ALL_TFS",all_df,ts)
    for tf in ["M1","M5","M15"]:
        sub=all_df[all_df["tf"]==tf].reset_index(drop=True)
        if len(sub): write_report(tf,sub,ts)
    print(f"\nFFT Cycle done. {len(all_df)} total rows.")

if __name__=="__main__":
    main()
