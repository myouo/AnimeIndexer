import sqlite3
from pathlib import Path
from .config import settings


def ensure_db_dir() -> None:
    db_path = Path(settings.db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)


def get_conn() -> sqlite3.Connection:
    ensure_db_dir()
    conn = sqlite3.connect(settings.db_path)
    conn.row_factory = sqlite3.Row
    return conn
