"""
Reusable MySQL connection utilities (SQLAlchemy + PyMySQL).

Credentials are read from environment variables only — never hardcoded.
Required: MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any
from urllib.parse import quote_plus

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

import python.config.env  # noqa: F401 — loads .env via dotenv

_REQUIRED_VARS = (
    "MYSQL_HOST",
    "MYSQL_DATABASE",
    "MYSQL_USER",
    "MYSQL_PASSWORD",
)


class DatabaseConfigError(ValueError):
    """Raised when required MySQL environment variables are missing."""


def get_mysql_settings() -> dict[str, str]:
    """Return MySQL connection settings from the environment."""
    missing = [key for key in _REQUIRED_VARS if not os.getenv(key)]
    if missing:
        raise DatabaseConfigError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Copy .env.example to .env and set MySQL values."
        )
    return {
        "host": os.environ["MYSQL_HOST"],
        "port": os.environ.get("MYSQL_PORT", "3306"),
        "database": os.environ["MYSQL_DATABASE"],
        "user": os.environ["MYSQL_USER"],
        "password": os.environ["MYSQL_PASSWORD"],
        "charset": os.environ.get("MYSQL_CHARSET", "utf8mb4"),
    }


def build_mysql_url() -> str:
    """Build a SQLAlchemy URL for mysql+pymysql (password URL-encoded)."""
    cfg = get_mysql_settings()
    password = quote_plus(cfg["password"])
    return (
        f"mysql+pymysql://{cfg['user']}:{password}"
        f"@{cfg['host']}:{cfg['port']}/{cfg['database']}"
        f"?charset={cfg['charset']}"
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Return a cached SQLAlchemy engine with connection health checks."""
    return create_engine(
        build_mysql_url(),
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
    )


def test_connection() -> dict[str, Any]:
    """
    Verify connectivity and return server metadata (no secrets).

    Raises:
        DatabaseConfigError: Missing env vars.
        SQLAlchemyError: Connection or query failed.
    """
    cfg = get_mysql_settings()
    engine = get_engine()
    with engine.connect() as conn:
        version_row = conn.execute(text("SELECT VERSION()")).one()
        db_row = conn.execute(text("SELECT DATABASE()")).one()

    return {
        "ok": True,
        "host": cfg["host"],
        "port": cfg["port"],
        "database": db_row[0] or cfg["database"],
        "user": cfg["user"],
        "server_version": version_row[0],
    }


def execute_sql(sql: str, params: dict[str, Any] | None = None) -> None:
    """Run a SQL statement (DDL/DML) in a transaction."""
    with get_engine().begin() as conn:
        conn.execute(text(sql), params or {})


def read_table(table_name: str, schema: str | None = None) -> pd.DataFrame:
    """Read a full table into a DataFrame (for exports and validation)."""
    engine = get_engine()
    qualified = f"`{schema}`.`{table_name}`" if schema else f"`{table_name}`"
    return pd.read_sql(f"SELECT * FROM {qualified}", engine)


def load_dataframe(
    df: pd.DataFrame,
    table_name: str,
    *,
    if_exists: str = "replace",
    chunksize: int = 1000,
) -> int:
    """
    Load a DataFrame into MySQL.

    Args:
        df: Data to load.
        table_name: Target table name (Power BI–friendly snake_case).
        if_exists: pandas.to_sql mode: 'fail', 'replace', or 'append'.
        chunksize: Rows per insert batch.

    Returns:
        Number of rows written.
    """
    if df.empty:
        return 0

    out = df.copy()
    # Normalize column names for MySQL / Power BI
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]

    out.to_sql(
        table_name,
        get_engine(),
        if_exists=if_exists,
        index=False,
        chunksize=chunksize,
        method="multi",
    )
    return len(out)


# Map cleaned parquet files → MySQL table names (star-schema friendly)
CLEANED_TO_MYSQL_TABLE: dict[str, str] = {
    "customers.parquet": "dim_customers",
    "subscriptions.parquet": "fact_subscriptions",
}
