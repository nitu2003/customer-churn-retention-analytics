"""
00 — Inspect raw CSV(s) and write a data profiling report.

Run from repository root (before or after placing files in data/raw/):
    python python/etl/00_profile_raw_data.py
"""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import pandas as pd

from python.config.paths import DATA_RAW, REPO_ROOT, ensure_dirs
from python.utils.io import read_table
from python.utils.schema import get_analysis_columns, profile_dataframe


REPORT_PATH = REPO_ROOT / "docs" / "data_profile_report.md"


def _md_table_from_df(df: pd.DataFrame, max_rows: int = 20) -> str:
    if df.empty:
        return "_None_\n"
    view = df.head(max_rows)
    headers = "| " + " | ".join(str(c) for c in view.columns) + " |"
    sep = "| " + " | ".join("---" for _ in view.columns) + " |"
    rows = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for row in view.itertuples(index=False, name=None)
    ]
    return "\n".join([headers, sep, *rows]) + "\n"


def render_report(profiles: list[dict]) -> str:
    lines = [
        "# Data profiling report",
        "",
        f"_Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}_",
        "",
    ]

    for p in profiles:
        ac = p["analysis_columns"]
        lines.extend([
            f"## Source: `{p['source_name']}`",
            "",
            f"| Metric | Value |",
            f"|--------|-------|",
            f"| Rows | {p['row_count']:,} |",
            f"| Columns | {p['column_count']} |",
            f"| Dataset type | {'IBM Telco-style churn' if p['is_telco'] else 'Generic churn CSV'} |",
            f"| ID column | `{p['id_column'] or '_(auto-generated)_'}` |",
            f"| **Churn target column** | **`{p['churn_column'] or '_(not detected)_'}`** |",
            f"| Duplicate IDs | {p['duplicate_ids'] if p['duplicate_ids'] is not None else 'N/A'} |",
            "",
            "### Churn target distribution",
            "",
        ])
        if p["churn_distribution"]:
            for k, v in sorted(p["churn_distribution"].items(), key=lambda x: -x[1]):
                lines.append(f"- `{k}`: {v:,}")
        else:
            lines.append("_No churn column detected._")
        lines.extend(["", "### Useful analysis columns", ""])

        for group, title in [
            ("demographics", "Demographics"),
            ("tenure_and_contract", "Tenure & contract"),
            ("services", "Products & services"),
            ("billing_and_revenue", "Billing & revenue"),
            ("numeric_features", "All numeric features"),
            ("categorical_features", "All categorical features"),
        ]:
            cols = ac.get(group, [])
            if cols and group in ("demographics", "tenure_and_contract", "services", "billing_and_revenue"):
                lines.append(f"**{title}:** `" + "`, `".join(cols) + "`")
                lines.append("")

        lines.extend([
            "### Column types",
            "",
            "| Column | Dtype |",
            "|--------|-------|",
        ])
        for col, dtype in p["dtypes"].items():
            lines.append(f"| `{col}` | {dtype} |")
        lines.append("")

        if not p["missing"].empty:
            lines.extend(["### Null counts", "", _md_table_from_df(p["missing"].reset_index().rename(columns={"index": "column"})), ""])
        if not p["blanks"].empty:
            lines.extend(["### Blank string counts", "", _md_table_from_df(p["blanks"].reset_index().rename(columns={"index": "column"})), ""])

        if not p["numeric_summary"].empty:
            lines.extend(["### Numeric summary (sample)", "", _md_table_from_df(p["numeric_summary"].reset_index().rename(columns={"index": "column"})), ""])

    lines.append("---\n\nSee `docs/02_data_sources.md` and `docs/03_metric_definitions.md` for lineage and metric definitions.\n")
    return "\n".join(lines)


def profile_raw_files() -> None:
    ensure_dirs()
    raw_files = sorted(DATA_RAW.glob("*.csv")) + sorted(DATA_RAW.glob("*.parquet"))
    if not raw_files:
        print(f"No files in {DATA_RAW}. Place telco_customer_churn.csv or run download script.")
        return

    profiles = []
    for path in raw_files:
        df = read_table(path)
        profiles.append(profile_dataframe(df, source_name=path.name))
        churn = profiles[-1]["churn_column"]
        print(f"Profiled {path.name}: {len(df):,} rows, churn column={churn!r}")

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(render_report(profiles), encoding="utf-8")
    print(f"\nReport written: {REPORT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    profile_raw_files()
