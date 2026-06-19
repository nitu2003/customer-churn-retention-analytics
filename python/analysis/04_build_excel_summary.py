"""
04 — Build executive Excel workbook from cleaned / mart data.
Run: python python/analysis/04_build_excel_summary.py
"""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd

from python.config.paths import DATA_CLEANED, OUTPUT_EXCEL, ensure_dirs
from python.utils.io import read_table


def build_summary() -> None:
    ensure_dirs()
    out_path = OUTPUT_EXCEL / "Churn_Executive_Summary.xlsx"

    sheets: dict[str, pd.DataFrame] = {}
    customers_path = DATA_CLEANED / "customers.parquet"
    if customers_path.exists():
        customers = read_table(customers_path)
        sheets["Customers"] = customers.head(1000)
        sheets["KPIs"] = pd.DataFrame(
            {
                "metric": ["Total customers (sample)", "Columns"],
                "value": [len(customers), len(customers.columns)],
            }
        )
    else:
        sheets["README"] = pd.DataFrame(
            {"note": ["Run ETL pipeline and re-generate this workbook."]}
        )

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    build_summary()
