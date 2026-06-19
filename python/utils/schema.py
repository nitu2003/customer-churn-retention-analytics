"""
Automatic schema detection for churn datasets (Telco-style and generic CSVs).
"""

from __future__ import annotations

import re
from typing import Any

import numpy as np
import pandas as pd

# Columns matching these patterns are treated as the churn target (first match wins)
CHURN_COLUMN_PATTERNS = (
    r"^churn$",
    r"^is_churn",
    r"^churned$",
    r"^attrition",
    r"^exited$",
    r"^leave$",
    r"^target$",
)

ID_COLUMN_PATTERNS = (
    r"^customer_?id$",
    r"^customerid$",
    r"^client_?id$",
    r"^account_?id$",
    r"^subscriber_?id$",
    r"^user_?id$",
)

# Excluded from "analysis feature" lists (identifiers + raw target text)
META_EXCLUDE_PATTERNS = (
    r"^customer_?id$",
    r"^customerid$",
    r"^id$",
    r"^churn$",
    r"^churn_label$",
)


def normalize_column_name(name: str) -> str:
    """Snake_case column names for SQL / Power BI compatibility."""
    s = str(name).strip()
    s = re.sub(r"[^\w]+", "_", s, flags=re.UNICODE)
    s = re.sub(r"_+", "_", s).strip("_").lower()
    return s


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [normalize_column_name(c) for c in out.columns]
    return out


def _match_column(columns: list[str], patterns: tuple[str, ...]) -> str | None:
    for col in columns:
        for pat in patterns:
            if re.search(pat, col, re.IGNORECASE):
                return col
    return None


def detect_id_column(columns: list[str]) -> str | None:
    return _match_column(columns, ID_COLUMN_PATTERNS)


def detect_churn_column(columns: list[str]) -> str | None:
    return _match_column(columns, CHURN_COLUMN_PATTERNS)


def is_telco_churn_dataset(columns: list[str]) -> bool:
    cols = {normalize_column_name(c) for c in columns}
    return "churn" in cols and (
        "customerid" in cols or "customer_id" in cols or "tenure" in cols
    )


def get_analysis_columns(
    df: pd.DataFrame,
    *,
    churn_col: str | None = None,
    id_col: str | None = None,
) -> dict[str, list[str]]:
    """
    Group columns useful for churn analysis.

    Returns dict with keys: demographics, tenure_and_contract,
    services, billing_and_revenue, numeric_features, categorical_features.
    """
    churn_col = churn_col or detect_churn_column(list(df.columns))
    id_col = id_col or detect_id_column(list(df.columns))

    feature_cols = []
    for c in df.columns:
        if c == churn_col or c == id_col:
            continue
        if c == "is_churned":
            continue
        if re.search(r"^churn_label$", c, re.I):
            continue
        if re.search(r"^customer_?id$", c, re.I):
            continue
        feature_cols.append(c)

    demographics = [c for c in feature_cols if re.search(
        r"gender|senior|partner|depend|age|marital", c, re.I
    )]
    tenure_contract = [c for c in feature_cols if re.search(
        r"tenure|contract|subscription", c, re.I
    )]
    services = [c for c in feature_cols if re.search(
        r"phone|internet|online|streaming|tech|device|multiple|service", c, re.I
    )]
    billing = [c for c in feature_cols if re.search(
        r"charge|payment|billing|paperless|invoice|mrr|revenue", c, re.I
    )]

    tagged = set(demographics + tenure_contract + services + billing)
    other = [c for c in feature_cols if c not in tagged]

    numeric = [c for c in feature_cols if pd.api.types.is_numeric_dtype(df[c])]
    categorical = [c for c in feature_cols if c not in numeric]

    return {
        "demographics": demographics,
        "tenure_and_contract": tenure_contract,
        "services": services,
        "billing_and_revenue": billing,
        "other_features": other,
        "numeric_features": numeric,
        "categorical_features": categorical,
        "all_features": feature_cols,
    }


def coerce_churn_target(series: pd.Series) -> pd.Series:
    """Map Yes/No, 1/0, True/False to boolean is_churned."""
    s = series.copy()
    if pd.api.types.is_bool_dtype(s):
        return s.astype(bool)
    if pd.api.types.is_numeric_dtype(s):
        return s.fillna(0).astype(int).astype(bool)
    normalized = s.astype(str).str.strip().str.lower()
    mapping = {
        "yes": True,
        "y": True,
        "true": True,
        "1": True,
        "churn": True,
        "no": False,
        "n": False,
        "false": False,
        "0": False,
    }
    return normalized.map(mapping)


def profile_dataframe(df: pd.DataFrame, source_name: str = "dataset") -> dict[str, Any]:
    """Build profiling statistics for markdown report generation."""
    df_norm = normalize_columns(df)
    churn_col = detect_churn_column(list(df_norm.columns))
    id_col = detect_id_column(list(df_norm.columns))
    analysis = get_analysis_columns(df_norm, churn_col=churn_col, id_col=id_col)

    missing = df_norm.isnull().sum()
    missing_pct = (missing / len(df_norm) * 100).round(2)
    missing_report = (
        pd.DataFrame({"nulls": missing, "pct": missing_pct})
        .query("nulls > 0")
        .sort_values("nulls", ascending=False)
    )

    blank_mask = df_norm.astype(str).apply(lambda col: col.str.strip() == "")
    blank_report = (
        pd.DataFrame({"blanks": blank_mask.sum(), "pct": (blank_mask.sum() / len(df_norm) * 100).round(2)})
        .query("blanks > 0")
        .sort_values("blanks", ascending=False)
    )

    churn_distribution = None
    if churn_col:
        churn_distribution = df_norm[churn_col].value_counts(dropna=False).to_dict()

    dtypes = df_norm.dtypes.astype(str).to_dict()
    numeric_summary = df_norm.describe(include="number").transpose() if analysis["numeric_features"] else pd.DataFrame()
    cat_summary = {}
    for col in analysis["categorical_features"][:15]:
        cat_summary[col] = df_norm[col].value_counts(dropna=False).head(5).to_dict()

    return {
        "source_name": source_name,
        "row_count": len(df_norm),
        "column_count": len(df_norm.columns),
        "columns": list(df_norm.columns),
        "dtypes": dtypes,
        "churn_column": churn_col,
        "id_column": id_col,
        "is_telco": is_telco_churn_dataset(list(df_norm.columns)),
        "analysis_columns": analysis,
        "missing": missing_report,
        "blanks": blank_report,
        "churn_distribution": churn_distribution,
        "numeric_summary": numeric_summary,
        "categorical_top_values": cat_summary,
        "duplicate_ids": (
            int(df_norm[id_col].duplicated().sum()) if id_col and id_col in df_norm.columns else None
        ),
    }


def clean_churn_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize any churn-style single-table dataset for analytics / MySQL load.
    """
    out = normalize_columns(df)
    id_col = detect_id_column(list(out.columns))
    churn_col = detect_churn_column(list(out.columns))

    if id_col and id_col != "customer_id":
        out = out.rename(columns={id_col: "customer_id"})
    elif id_col is None and "customer_id" not in out.columns:
        out.insert(0, "customer_id", [f"ROW-{i:06d}" for i in range(len(out))])

    if "customer_id" in out.columns:
        out["customer_id"] = out["customer_id"].astype(str)

    if churn_col:
        out["is_churned"] = coerce_churn_target(out[churn_col])
        if churn_col != "churn_label":
            out["churn_label"] = out[churn_col].astype(str)
        if churn_col not in ("churn_label", "is_churned"):
            out = out.drop(columns=[churn_col])

    if "total_charges" in out.columns:
        out["total_charges"] = pd.to_numeric(
            out["total_charges"].replace(r"^\s*$", np.nan, regex=True),
            errors="coerce",
        )

    if "monthly_charges" in out.columns:
        out["monthly_charges"] = pd.to_numeric(out["monthly_charges"], errors="coerce")

    if "tenure" in out.columns:
        out["tenure"] = pd.to_numeric(out["tenure"], errors="coerce").astype("Int64")

    if "senior_citizen" in out.columns:
        out["senior_citizen"] = out["senior_citizen"].astype(int)

    return out
