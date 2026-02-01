from typing import List, Optional, Tuple
from ..db import get_conn


def search_anime(
    keyword: Optional[str],
    tags: Optional[List[str]],
    limit: int,
    offset: int,
) -> Tuple[int, list]:
    conn = get_conn()
    where = []
    params: list = []

    if keyword:
        where.append("(title LIKE ? OR title_original LIKE ?)")
        like = f"%{keyword}%"
        params.extend([like, like])

    if tags:
        placeholders = ",".join(["?"] * len(tags))
        where.append(
            f"id IN ("
            f"SELECT anime_id FROM anime_tag at "
            f"JOIN tag t ON t.id = at.tag_id "
            f"WHERE t.name IN ({placeholders}) "
            f"GROUP BY anime_id "
            f"HAVING COUNT(DISTINCT t.name) = {len(tags)}"
            f")"
        )
        params.extend(tags)

    where_sql = " AND ".join(where) if where else "1=1"

    count_sql = f"SELECT COUNT(*) AS c FROM anime WHERE {where_sql}"
    total = conn.execute(count_sql, params).fetchone()["c"]

    sql = (
        f"SELECT id, title, title_original, author, description, score, cover_url, air_date "
        f"FROM anime WHERE {where_sql} "
        f"ORDER BY score DESC NULLS LAST, id DESC "
        f"LIMIT ? OFFSET ?"
    )
    rows = conn.execute(sql, params + [limit, offset]).fetchall()
    conn.close()
    return total, [dict(r) for r in rows]


def get_anime_detail(anime_id: int) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute(
        "SELECT id, title, title_original, author, description, score, cover_url, air_date "
        "FROM anime WHERE id = ?",
        (anime_id,),
    ).fetchone()
    if not row:
        conn.close()
        return None
    tags = conn.execute(
        "SELECT t.name FROM tag t "
        "JOIN anime_tag at ON t.id = at.tag_id "
        "WHERE at.anime_id = ? ORDER BY t.name",
        (anime_id,),
    ).fetchall()
    conn.close()
    data = dict(row)
    data["tags"] = [t["name"] for t in tags]
    return data
