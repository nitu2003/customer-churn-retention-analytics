"""
Test MySQL connectivity using credentials from .env.

Run from repository root:
    python python/scripts/test_db_connection.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from sqlalchemy.exc import SQLAlchemyError

from python.utils.db import DatabaseConfigError, test_connection


def main() -> int:
    print("Testing MySQL connection (credentials from .env)...")
    try:
        info = test_connection()
    except DatabaseConfigError as exc:
        print(f"Configuration error: {exc}")
        return 1
    except SQLAlchemyError as exc:
        print(f"Connection failed: {exc}")
        print("\nCheck that MySQL is running and .env values are correct.")
        return 1

    print("Connection successful.")
    print(f"  Host:     {info['host']}:{info['port']}")
    print(f"  Database: {info['database']}")
    print(f"  User:     {info['user']}")
    print(f"  Server:   {info['server_version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
