"""
01 — Exploratory analysis on cleaned data (console summary).
Run: python python/analysis/01_churn_eda.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.config.paths import DATA_CLEANED, ensure_dirs
from python.utils.io import read_table


def eda() -> None:
    ensure_dirs()
    customers_path = DATA_CLEANED / "customers.parquet"
    if not customers_path.exists():
        print("customers.parquet not found. Complete ETL first.")
        return

    customers = read_table(customers_path)
    print("=== Customer EDA ===")
    print(customers.describe(include="all").T.head(20))
    print(f"\nShape: {customers.shape}")


if __name__ == "__main__":
    eda()
