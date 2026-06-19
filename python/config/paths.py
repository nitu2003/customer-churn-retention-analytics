"""Central path configuration for the churn analytics platform."""

from pathlib import Path
import os

from python.config.env import REPO_ROOT  # noqa: F401 — triggers load_dotenv


def _resolve_path(env_key: str, default: Path) -> Path:
    value = os.getenv(env_key)
    if not value:
        return default
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


DATA_RAW = _resolve_path("DATA_RAW_DIR", REPO_ROOT / "data" / "raw")
DATA_CLEANED = _resolve_path("DATA_CLEANED_DIR", REPO_ROOT / "data" / "cleaned")
OUTPUT_EXCEL = _resolve_path("OUTPUT_EXCEL_DIR", REPO_ROOT / "outputs" / "excel")
OUTPUT_CHARTS = _resolve_path("OUTPUT_CHARTS_DIR", REPO_ROOT / "outputs" / "charts")
POWERBI_EXPORT = _resolve_path("POWERBI_EXPORT_DIR", REPO_ROOT / "powerbi" / "exports")


def ensure_dirs() -> None:
    """Create output directories if they do not exist."""
    for path in (DATA_RAW, DATA_CLEANED, OUTPUT_EXCEL, OUTPUT_CHARTS, POWERBI_EXPORT):
        path.mkdir(parents=True, exist_ok=True)
