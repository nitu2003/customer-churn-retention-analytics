"""
Deploy MySQL analytics + Power BI views from sql/mysql/.

Run from repository root (requires dim_customers populated):
    python python/scripts/deploy_mysql_views.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text

from python.config.paths import REPO_ROOT
from python.utils.db import DatabaseConfigError, get_engine

SQL_DIRS = (
    REPO_ROOT / "sql" / "mysql" / "analytics",
    REPO_ROOT / "sql" / "mysql" / "power_bi",
)


def _split_statements(sql: str) -> list[str]:
    """Split on semicolons outside simple single-quoted strings."""
    statements: list[str] = []
    current: list[str] = []
    in_string = False
    for line in sql.splitlines():
        stripped = line.strip()
        if stripped.startswith("--") or not stripped:
            continue
        current.append(line)
        quote_count = line.count("'") - line.count("\\'")
        if quote_count % 2 == 1:
            in_string = not in_string
        if not in_string and ";" in line:
            stmt = "\n".join(current).strip()
            if stmt.endswith(";"):
                stmt = stmt[:-1].strip()
            if stmt:
                statements.append(stmt)
            current = []
    tail = "\n".join(current).strip()
    if tail:
        if tail.endswith(";"):
            tail = tail[:-1].strip()
        statements.append(tail)
    return statements


def deploy() -> None:
    engine = get_engine()
    files = []
    for folder in SQL_DIRS:
        files.extend(sorted(folder.glob("*.sql")))

    if not files:
        print("No SQL files found under sql/mysql/")
        return

    with engine.begin() as conn:
        for path in files:
            sql = path.read_text(encoding="utf-8")
            statements = _split_statements(sql)
            print(f"\n{path.relative_to(REPO_ROOT)} ({len(statements)} statements)")
            for stmt in statements:
                conn.execute(text(stmt))
            print(f"  OK")

    print("\nDeployed analytics + Power BI views.")
    print("Power BI: connect to MySQL and import views prefixed with vw_pbi_")


if __name__ == "__main__":
    try:
        deploy()
    except DatabaseConfigError as exc:
        print(f"Configuration error: {exc}")
        sys.exit(1)
