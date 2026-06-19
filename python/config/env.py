"""Load environment variables from .env at repository root."""

from pathlib import Path

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parents[2]

# Idempotent: safe to call from multiple modules
load_dotenv(REPO_ROOT / ".env", override=False)
