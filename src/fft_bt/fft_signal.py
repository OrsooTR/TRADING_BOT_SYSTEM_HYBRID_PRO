"""
FFT signal computation for trading.

Concept (from Song et al., 2014 - SSRN-2487656):
  - Apply FFT to a rolling price window
  - Dominant low-frequency components = underlying trend / cycle
  - Reconstruct signal keeping only lowest N frequency components
  - Price > FFT_trend  →  bullish bias (LONG)
  - Price < FFT_trend  →  bearish bias (SHORT)
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view


def compute_fft_trend(
    closes: np.ndarray,
    window: int,
    n_dominant: int,
    chunk_size: int = 40_000,
) -> np.ndarray:
    """
    Rolling FFT low-pass filter.

    For each bar i, takes the last `window` closes, applies FFT,
    zeroes out all components beyond the `n_dominant` lowest frequencies,
    inverse-FFTs and returns the last value as the trend estimate.

    Uses chunked sliding_window_view for memory efficiency.

    Parameters
    ----------
    closes      : 1-D price array
    window      : rolling window length
    n_dominant  : number of dominant frequency bins to keep (DC + n_dominant)
    chunk_size  : bars processed per chunk (controls RAM usage)

    Returns
    -------
    trend : array of same length as closes, NaN for first (window-1) bars
    """
    n = len(closes)
    trend = np.full(n, np.nan, dtype=np.float64)

    start = window - 1          # first valid output index
    for chunk_start in range(start, n, chunk_size):
        chunk_end = min(chunk_start + chunk_size, n)
        data_start = chunk_start - window + 1

        chunk_data = closes[data_start:chunk_end]
        if len(chunk_data) < window:
            continue

        # shape: (n_windows, window)  where n_windows = chunk_end - chunk_start
        views = sliding_window_view(chunk_data, window)

        # Batch FFT  shape: (n_windows, window//2 + 1)
        ffts = np.fft.rfft(views, axis=1)

        # Zero out high-frequency bins beyond n_dominant
        if n_dominant + 1 < ffts.shape[1]:
            ffts[:, n_dominant + 1:] = 0

        # Batch IFFT
        reconstructed = np.fft.irfft(ffts, n=window, axis=1)

        # Last value of each reconstructed window = current trend estimate
        n_out = chunk_end - chunk_start
        trend[chunk_start:chunk_end] = reconstructed[:n_out, -1]

    return trend


def compute_atr(
    high: np.ndarray,
    low: np.ndarray,
    close: np.ndarray,
    period: int = 14,
) -> np.ndarray:
    """Wilder ATR (same formula used by backtrader bt.ind.ATR)."""
    n = len(close)
    tr = np.empty(n, dtype=np.float64)
    tr[0] = high[0] - low[0]
    prev_close = close[:-1]
    tr[1:] = np.maximum(
        high[1:] - low[1:],
        np.maximum(np.abs(high[1:] - prev_close), np.abs(low[1:] - prev_close)),
    )
    # Wilder smoothing (EMA with alpha=1/period)
    atr = np.empty(n, dtype=np.float64)
    atr[:period] = np.nan
    atr[period - 1] = tr[:period].mean()
    alpha = 1.0 / period
    for i in range(period, n):
        atr[i] = atr[i - 1] * (1 - alpha) + tr[i] * alpha
    return atr


def build_fft_frame(
    df: pd.DataFrame,
    window: int,
    n_dominant: int,
    atr_period: int = 14,
) -> pd.DataFrame:
    """
    Augments df with columns:
      fft_trend : low-pass reconstructed price trend
      atr       : Wilder ATR(14)
      fft_dir   : +1 (price > trend) or -1 (price < trend)

    Returns a copy of df with the new columns, NaN rows dropped.
    """
    out = df.copy()
    closes = df["close"].values
    out["fft_trend"] = compute_fft_trend(closes, window, n_dominant)
    out["atr"] = compute_atr(
        df["high"].values, df["low"].values, closes, atr_period
    )
    out["fft_dir"] = np.where(out["close"] > out["fft_trend"], 1.0, -1.0)
    # First valid row = max(window-1, atr_period-1)
    warmup = max(window - 1, atr_period - 1)
    out.iloc[:warmup] = np.nan
    return out.dropna(subset=["fft_trend", "atr"])
