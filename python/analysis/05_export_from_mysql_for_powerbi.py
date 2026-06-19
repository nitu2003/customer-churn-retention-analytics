"""
05 — Export MySQL tables to CSV for Power BI (Import mode).

Use after python/etl/04_load_to_mysql.py, or whenever MySQL is the source of truth.

Run from repository root:
    python python/analysis/05_export_from_mysql_for_powerbi.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd
from sqlalchemy import inspect

from python.config.paths import POWERBI_EXPORT, ensure_dirs
from python.utils.db import get_engine, get_mysql_settings
from python.utils.io import write_csv_for_powerbi


# Tables to export for the star schema (extend as you add marts in MySQL)
POWERBI_TABLES = (
    "dim_customers",
    "fact_subscriptions",
    "dim_date",  # created locally if missing in MySQL
)


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
    engine = get_engine()
    inspector = inspect(engine)
    existing = set(inspector.get_table_names())

    for table in POWERBI_TABLES:
        dest = POWERBI_EXPORT / f"{table}.csv"
        if table == "dim_date" and table not in existing:
            write_csv_for_powerbi(build_dim_date(), dest)
            print(f"Exported {dest.name} (generated date dimension)")
            continue
        if table not in existing:
            print(f"Skipped {table} — not found in MySQL")
            continue
        df = pd.read_sql(f"SELECT * FROM `{table}`", engine)
        write_csv_for_powerbi(df, dest)
        print(f"Exported {dest.name} ({len(df):,} rows from MySQL)")

    cfg = get_mysql_settings()
    print("\nPower BI options:")
    print(f"  1. Import CSV from: {POWERBI_EXPORT}")
    print(
        f"  2. DirectQuery: MySQL -> {cfg['host']}:{cfg['port']} / {cfg['database']}"
    )
    print("  See powerbi/DATA_MODEL.md for relationships and measures.")


if __name__ == "__main__":
    export()
