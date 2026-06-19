# Python scripts

Run from repository root:

```bash
# 1. Verify MySQL (.env must be configured)
python python/scripts/test_db_connection.py

# 2. Profile + ETL: raw -> cleaned -> MySQL
python python/etl/00_profile_raw_data.py
python python/etl/01_ingest_raw.py
python python/etl/02_clean_and_validate.py
python python/etl/03_run_quality_checks.py
python python/etl/04_load_to_mysql.py

# 3. Analysis & outputs
python python/analysis/01_churn_eda.py
python python/analysis/02_generate_charts.py
python python/analysis/05_export_from_mysql_for_powerbi.py
python python/analysis/04_build_excel_summary.py
```

Modules use `python/config/paths.py` and `python/utils/db.py` (SQLAlchemy + PyMySQL, credentials from `.env` only).
