"""
03 — Export dimension and fact tables for Power BI import.
Run: python python/analysis/03_export_for_powerbi.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd

from python.config.paths import DATA_CLEANED, POWERBI_EXPORT, ensure_dirs
from python.utils.io import read_table, write_csv_for_powerbi


def build_dim_date(start: str = "2020-01-01", end: str = "2026-12-31") -> pd.DataFrame:
    dates = pd.date_range(start, end, freq="D")
    return pd.DataFrame(
        {
            "date": dates,
            "year": dates.year,
            "month": dates.month,
            "month_name": dates.strftime("%B"),
            "year_month": dates.strftime("%Y-%m"),
            "is_month_end": dates.is_month_end,
        }
    )


def export() -> None:
    ensure_dirs()
    write_csv_for_powerbi(build_dim_date(), POWERBI_EXPORT / "dim_date.csv")
    print("Exported dim_date.csv")

    mapping = {
        "customers.parquet": "dim_customer.csv",
        "subscriptions.parquet": "fact_subscriptions.csv",
    }
    for src, dest in mapping.items():
        path = DATA_CLEANED / src
        if path.exists():
            write_csv_for_powerbi(read_table(path), POWERBI_EXPORT / dest)
            print(f"Exported {dest}")
        else:
            print(f"Skipped {dest} — {src} not found")

    print(f"\nPower BI: Get Data from {POWERBI_EXPORT}")
    print("See powerbi/DATA_MODEL.md for relationships and measures.")


if __name__ == "__main__":
    export()
