from pathlib import Path
from .db import get_conn


ANIME_COLUMNS = {
    "type": "INTEGER",
    "name": "TEXT",
    "name_cn": "TEXT",
    "title": "TEXT NOT NULL",
    "title_original": "TEXT",
    "summary": "TEXT",
    "score": "REAL",
    "rank": "INTEGER",
    "rating_total": "INTEGER",
    "rating_count_total": "INTEGER",
    "cover_url": "TEXT",
    "date": "TEXT",
    "platform": "TEXT",
    "nsfw": "INTEGER",
    "series": "INTEGER",
    "locked": "INTEGER",
    "eps": "INTEGER",
    "total_episodes": "INTEGER",
    "volumes": "INTEGER",
    "images_json": "TEXT",
    "infobox_json": "TEXT",
    "meta_tags_json": "TEXT",
    "rating_json": "TEXT",
    "collection_json": "TEXT",
    "raw_json": "TEXT",
    "updated_at": "TEXT",
}


def init_db() -> None:
    schema = Path(__file__).resolve().parent.parent / "schema.sql"
    with open(schema, "r", encoding="utf-8") as f:
        sql = f.read()
    conn = get_conn()
    conn.executescript(sql)

    # Basic migrations for existing databases
    existing = {row[1] for row in conn.execute("PRAGMA table_info(anime)")}
    for col, col_type in ANIME_COLUMNS.items():
        if col not in existing:
            conn.execute(f"ALTER TABLE anime ADD COLUMN {col} {col_type}")

    existing_at = {row[1] for row in conn.execute("PRAGMA table_info(anime_tag)")}
    if "tag_count" not in existing_at:
        conn.execute("ALTER TABLE anime_tag ADD COLUMN tag_count INTEGER")

    conn.execute(
        "CREATE TABLE IF NOT EXISTS sync_state (key TEXT PRIMARY KEY, value TEXT)"
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
