"""
Download IBM Telco Customer Churn CSV into data/raw/ if not present.

Run from repository root:
    python python/scripts/download_telco_dataset.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import urlretrieve

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from python.config.paths import DATA_RAW, ensure_dirs

TELCO_URL = (
    "https://raw.githubusercontent.com/IBM/"
    "telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
)
OUTPUT_NAME = "telco_customer_churn.csv"


def download() -> Path:
    ensure_dirs()
    dest = DATA_RAW / OUTPUT_NAME
    if dest.exists():
        print(f"Already exists: {dest}")
        return dest
    print(f"Downloading from IBM open dataset...")
    urlretrieve(TELCO_URL, dest)  # noqa: S310 — trusted public URL for portfolio dataset
    print(f"Saved: {dest}")
    return dest


if __name__ == "__main__":
    download()
