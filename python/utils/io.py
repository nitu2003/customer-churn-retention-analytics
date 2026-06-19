"""Shared I/O helpers for parquet and CSV."""

from pathlib import Path

import pandas as pd


def read_table(path: Path) -> pd.DataFrame:
    """Read parquet or CSV based on file extension."""
    suffix = path.suffix.lower()
    if suffix == ".parquet":
        return pd.read_parquet(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {path}")


def write_parquet(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)


def write_csv_for_powerbi(df: pd.DataFrame, path: Path) -> None:
    """UTF-8 CSV suitable for Power BI import."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False, encoding="utf-8-sig")
