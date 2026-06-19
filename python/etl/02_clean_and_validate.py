"""
02 — Clean, standardize, and write analysis-ready tables to data/cleaned/.
Supports IBM Telco-style single-table churn CSVs and generic customer/subscription files.

Run: python python/etl/02_clean_and_validate.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd

from python.config.paths import DATA_CLEANED, DATA_RAW, ensure_dirs
from python.utils.io import read_table, write_parquet
from python.utils.schema import clean_churn_dataset, detect_churn_column, is_telco_churn_dataset


def clean_customers_legacy(df: pd.DataFrame) -> pd.DataFrame:
    """Legacy path for multi-file customer extracts."""
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    if "customer_id" in out.columns:
        out["customer_id"] = out["customer_id"].astype(str)
    return out


def clean_subscriptions(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip().lower().replace(" ", "_") for c in out.columns]
    for col in ("start_date", "end_date"):
        if col in out.columns:
            out[col] = pd.to_datetime(out[col], errors="coerce")
    return out


def _is_churn_single_table(name: str, df: pd.DataFrame) -> bool:
    normalized = [c.strip().lower().replace(" ", "_") for c in df.columns]
    return (
        "churn" in name
        or "telco" in name
        or is_telco_churn_dataset(df.columns)
        or detect_churn_column(list(df.columns)) is not None
        or detect_churn_column(normalized) is not None
    )


def clean() -> None:
    ensure_dirs()
    staging_dir = DATA_RAW.parent / "staging"
    if not staging_dir.exists():
        print("Run 01_ingest_raw.py first.")
        return

    wrote_customers = False
    for path in staging_dir.glob("*.parquet"):
        df = read_table(path)
        name = path.stem.lower()

        if _is_churn_single_table(name, df):
            cleaned = clean_churn_dataset(df)
            write_parquet(cleaned, DATA_CLEANED / "customers.parquet")
            churn_rate = cleaned["is_churned"].mean() * 100 if "is_churned" in cleaned.columns else 0
            print(
                f"Wrote customers.parquet ({len(cleaned):,} rows, "
                f"churn rate {churn_rate:.1f}%)"
            )
            wrote_customers = True
        elif "customer" in name and "month" not in name and "churn" not in name:
            cleaned = clean_customers_legacy(df)
            write_parquet(cleaned, DATA_CLEANED / "customers.parquet")
            print(f"Wrote customers.parquet ({len(cleaned):,} rows)")
            wrote_customers = True
        elif "subscription" in name:
            cleaned = clean_subscriptions(df)
            write_parquet(cleaned, DATA_CLEANED / "subscriptions.parquet")
            print(f"Wrote subscriptions.parquet ({len(cleaned):,} rows)")
        else:
            cleaned = clean_churn_dataset(df)
            out_name = "customers.parquet" if detect_churn_column(list(cleaned.columns)) or "is_churned" in cleaned.columns else path.name
            write_parquet(cleaned, DATA_CLEANED / out_name)
            print(f"Wrote {out_name} ({len(cleaned):,} rows)")

    if not wrote_customers:
        print("No customer/churn table produced. Check data/raw/ and re-run 01_ingest_raw.py.")


if __name__ == "__main__":
    clean()
