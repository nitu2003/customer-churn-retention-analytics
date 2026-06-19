"""
02 — Generate static charts for portfolio and reports.
Run: python python/analysis/02_generate_charts.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import matplotlib.pyplot as plt
import pandas as pd

from python.config.paths import DATA_CLEANED, OUTPUT_CHARTS, ensure_dirs
from python.utils.io import read_table


def plot_placeholder_churn_trend() -> None:
    """Replace with real monthly churn from mart when available."""
    months = pd.date_range("2024-01-01", periods=12, freq="MS")
    rates = [2.1, 2.3, 2.0, 2.5, 2.8, 2.4, 2.2, 2.6, 2.9, 2.7, 2.5, 2.4]
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(months, rates, marker="o", linewidth=2, color="#2563eb")
    ax.set_title("Monthly Churn Rate (%) — template")
    ax.set_xlabel("Month")
    ax.set_ylabel("Churn rate %")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    out = OUTPUT_CHARTS / "churn_rate_monthly.png"
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"Saved {out}")


def generate() -> None:
    ensure_dirs()
    if (DATA_CLEANED / "customers.parquet").exists():
        _ = read_table(DATA_CLEANED / "customers.parquet")
    plot_placeholder_churn_trend()
    print("Add cohort heatmap and segment charts once marts are populated.")


if __name__ == "__main__":
    generate()
