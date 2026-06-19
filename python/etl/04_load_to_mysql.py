"""
04 — Load cleaned parquet files into MySQL tables.

Prerequisites:
  - .env configured with MYSQL_* variables
  - python/scripts/test_db_connection.py passes
  - python/etl/02_clean_and_validate.py completed

Run from repository root:
    python python/etl/04_load_to_mysql.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.config.paths import DATA_CLEANED, ensure_dirs
from python.utils.db import CLEANED_TO_MYSQL_TABLE, DatabaseConfigError, load_dataframe
from python.utils.io import read_table


def load_all(if_exists: str = "replace") -> None:
    ensure_dirs()
    files = list(DATA_CLEANED.glob("*.parquet"))
    if not files:
        print(f"No parquet files in {DATA_CLEANED}. Run 02_clean_and_validate.py first.")
        return

    loaded = 0
    for path in files:
        table_name = CLEANED_TO_MYSQL_TABLE.get(
            path.name,
            path.stem.lower().replace("-", "_"),
        )
        df = read_table(path)
        rows = load_dataframe(df, table_name, if_exists=if_exists)
        print(f"Loaded {path.name} -> `{table_name}` ({rows:,} rows)")
        loaded += 1

    if loaded:
        print(
            "\nMySQL tables are ready for Power BI:"
            "\n  - Direct: Get Data -> MySQL database -> select tables"
            "\n  - Or run: python python/analysis/05_export_from_mysql_for_powerbi.py"
        )


if __name__ == "__main__":
    try:
        load_all()
    except DatabaseConfigError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)
