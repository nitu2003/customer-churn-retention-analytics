"""
03 — Data quality checks on cleaned tables.
Run: python python/etl/03_run_quality_checks.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.config.paths import DATA_CLEANED, ensure_dirs
from python.utils.io import read_table


def check_not_null(df, column: str) -> bool:
    if column not in df.columns:
        print(f"  [SKIP] Column '{column}' not found")
        return True
    nulls = df[column].isna().sum()
    ok = nulls == 0
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {column}: {nulls} nulls")
    return ok


def check_unique(df, column: str) -> bool:
    if column not in df.columns:
        return True
    dupes = df[column].duplicated().sum()
    ok = dupes == 0
    status = "PASS" if ok else "FAIL"
    print(f"  [{status}] {column}: {dupes} duplicates")
    return ok


def run_checks() -> None:
    ensure_dirs()
    files = list(DATA_CLEANED.glob("*.parquet"))
    if not files:
        print(f"No cleaned files in {DATA_CLEANED}. Run 02_clean_and_validate.py first.")
        return

    all_passed = True
    for path in files:
        print(f"\nChecking {path.name}...")
        df = read_table(path)
        print(f"  Rows: {len(df):,}, Columns: {len(df.columns)}")
        if "customers" in path.name:
            all_passed &= check_not_null(df, "customer_id")
            all_passed &= check_unique(df, "customer_id")
            if "is_churned" in df.columns:
                all_passed &= check_not_null(df, "is_churned")
                churn_pct = df["is_churned"].mean() * 100
                print(f"  [INFO] churn rate (is_churned): {churn_pct:.2f}%")
        if "subscriptions" in path.name:
            all_passed &= check_not_null(df, "customer_id")

    print("\n" + ("All checks passed." if all_passed else "Some checks failed — see docs/05_data_quality_log.md"))


if __name__ == "__main__":
    run_checks()
