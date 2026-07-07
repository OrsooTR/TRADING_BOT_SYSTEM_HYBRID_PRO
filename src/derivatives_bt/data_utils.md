# Code Doc - data_utils.py

## Source
- `src/derivatives_bt/data_utils.py`
- [Apri il file Python sorgente](data_utils.py)
- [Torna all indice del codice](../../Pipeline_01/12_CODE/INDEX.md)

## Scopo
Utility di caricamento, merge, resampling e split dei dataset HistData usati nei backtest.

## Punti Chiave
- Legge i file ASCII compressi in zip e li converte in DataFrame OHLCV ordinati.
- Gestisce il resampling a M1, M5 e M15.
- Fornisce lo split train/OOS usato dal runner dei backtest.

## Collegamenti
- [INDEX](../../Pipeline_01/02_DATA/INDEX.md)
- [data_pipeline](../../Pipeline_01/02_DATA/data_pipeline.md)
- [02_Derivative_1st_2nd_Order](../../Pipeline_01/03_STRATEGIES/TESTED/02_Derivative_1st_2nd_Order.md)

## Codice Completo
```python
from __future__ import annotations

from pathlib import Path
from zipfile import ZipFile

import pandas as pd


HISTDATA_COLUMNS = ["datetime", "open", "high", "low", "close", "volume"]
TIMEFRAME_RULES = {
    "M1": "1min",
    "M5": "5min",
    "M15": "15min",
}


def _read_histdata_csv_from_zip(zip_path: Path) -> pd.DataFrame:
    with ZipFile(zip_path) as archive:
        csv_members = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not csv_members:
            raise FileNotFoundError(f"No CSV file found inside {zip_path}")

        with archive.open(csv_members[0]) as handle:
            frame = pd.read_csv(
                handle,
                sep=";",
                header=None,
                names=HISTDATA_COLUMNS,
                dtype={
                    "open": "float64",
                    "high": "float64",
                    "low": "float64",
                    "close": "float64",
                    "volume": "float64",
                },
            )

    frame["datetime"] = pd.to_datetime(frame["datetime"], format="%Y%m%d %H%M%S")
    return frame


def load_histdata_zips(zip_paths: list[str | Path]) -> pd.DataFrame:
    frames = [_read_histdata_csv_from_zip(Path(path)) for path in zip_paths]
    merged = pd.concat(frames, ignore_index=True)
    merged = merged.sort_values("datetime").drop_duplicates(subset="datetime", keep="last")
    merged = merged.set_index("datetime")
    merged.index = pd.DatetimeIndex(merged.index, name="datetime")
    return merged


def resample_ohlcv(frame: pd.DataFrame, timeframe: str) -> pd.DataFrame:
    timeframe = timeframe.upper()
    if timeframe not in TIMEFRAME_RULES:
        raise ValueError(f"Unsupported timeframe: {timeframe}")

    if timeframe == "M1":
        return frame.copy()

    resampled = frame.resample(TIMEFRAME_RULES[timeframe]).agg(
        {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
    )
    return resampled.dropna()


def split_frame(
    frame: pd.DataFrame,
    train_start: str,
    train_end: str,
    oos_start: str,
    oos_end: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    train = frame.loc[train_start:train_end].copy()
    oos = frame.loc[oos_start:oos_end].copy()
    return train, oos
```
