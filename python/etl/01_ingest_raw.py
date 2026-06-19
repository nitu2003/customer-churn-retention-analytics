"""
01 — Ingest raw files from data/raw into typed staging frames.
Run: python python/etl/01_ingest_raw.py
"""

from pathlib import Path
import sys

# Allow imports when run as script from repo root
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.config.paths import DATA_RAW, ensure_dirs
from python.utils.io import read_table, write_parquet


def ingest() -> None:
    ensure_dirs()
    raw_files = list(DATA_RAW.glob("*.csv")) + list(DATA_RAW.glob("*.parquet"))
    if not raw_files:
        print(f"No raw files found in {DATA_RAW}. Add source data and re-run.")
        return

    staging_dir = DATA_RAW.parent / "staging"
    staging_dir.mkdir(exist_ok=True)

    for path in raw_files:
        df = read_table(path)
        out = staging_dir / f"{path.stem}.parquet"
        write_parquet(df, out)
        print(f"Ingested {path.name} -> {out.relative_to(DATA_RAW.parents[1])} ({len(df):,} rows)")


if __name__ == "__main__":
    ingest()
