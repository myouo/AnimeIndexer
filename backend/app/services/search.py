import json
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
        where.append("(title LIKE ? OR title_original LIKE ? OR name LIKE ? OR name_cn LIKE ?)")
        like = f"%{keyword}%"
        params.extend([like, like, like, like])

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
        "SELECT id, title, title_original, name, name_cn, summary, summary AS description, "
        "score, rank, cover_url, date, platform "
        f"FROM anime WHERE {where_sql} "
        "ORDER BY score DESC NULLS LAST, id DESC "
        "LIMIT ? OFFSET ?"
    )
    rows = conn.execute(sql, params + [limit, offset]).fetchall()
    conn.close()
    return total, [dict(r) for r in rows]


def get_anime_detail(anime_id: int) -> Optional[dict]:
    conn = get_conn()
    row = conn.execute(
        "SELECT id, title, title_original, name, name_cn, summary, summary AS description, "
        "score, rank, cover_url, date, platform, "
        "images_json, infobox_json, meta_tags_json, rating_json, collection_json, raw_json "
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

    for key in [
        "images_json",
        "infobox_json",
        "meta_tags_json",
        "rating_json",
        "collection_json",
        "raw_json",
    ]:
        if data.get(key):
            try:
                data[key] = json.loads(data[key])
            except json.JSONDecodeError:
                data[key] = None
        else:
            data[key] = None

    data["images"] = data.pop("images_json")
    data["infobox"] = data.pop("infobox_json")
    data["meta_tags"] = data.pop("meta_tags_json")
    data["rating"] = data.pop("rating_json")
    data["collection"] = data.pop("collection_json")
    data["raw"] = data.pop("raw_json")
    return data
