from pathlib import Path
from .db import get_conn


def init_db() -> None:
    schema = Path(__file__).resolve().parent.parent / "schema.sql"
    with open(schema, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = get_conn()
    conn.executescript(sql)
    conn.close()


if __name__ == "__main__":
    init_db()
