import json
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple

import httpx

from ..config import settings
from ..db import get_conn


def _headers() -> Dict[str, str]:
    headers = {
        "User-Agent": settings.user_agent,
        "Accept": "application/json",
    }
    if settings.bangumi_access_token:
        headers["Authorization"] = f"Bearer {settings.bangumi_access_token}"
    return headers


def _rating_count_total(rating: Optional[dict]) -> Optional[int]:
    if not rating:
        return None
    count = rating.get("count")
    if not isinstance(count, dict):
        return None
    total = 0
    for v in count.values():
        try:
            total += int(v)
        except (TypeError, ValueError):
            continue
    return total


def _upsert_anime(conn, item: dict) -> None:
    rating = item.get("rating") or {}
    score = rating.get("score")
    if score is None:
        score = 0.0

    if score < 3.0:
        conn.execute("DELETE FROM anime WHERE id = ?", (item.get("id"),))
        conn.execute("DELETE FROM anime_tag WHERE anime_id = ?", (item.get("id"),))
        return

    name = item.get("name")
    name_cn = item.get("name_cn")
    title = name_cn or name or ""
    images = item.get("images") or {}
    cover_url = images.get("common") or images.get("medium") or images.get("large")

    payload = {
        "id": item.get("id"),
        "type": item.get("type"),
        "name": name,
        "name_cn": name_cn,
        "title": title,
        "title_original": name,
        "summary": item.get("summary"),
        "score": score,
        "rank": rating.get("rank"),
        "rating_total": rating.get("total"),
        "rating_count_total": _rating_count_total(rating),
        "cover_url": cover_url,
        "date": item.get("date"),
        "platform": item.get("platform"),
        "nsfw": 1 if item.get("nsfw") else 0,
        "series": 1 if item.get("series") else 0,
        "locked": 1 if item.get("locked") else 0,
        "eps": item.get("eps"),
        "total_episodes": item.get("total_episodes"),
        "volumes": item.get("volumes"),
        "images_json": json.dumps(images, ensure_ascii=False),
        "infobox_json": json.dumps(item.get("infobox") or [], ensure_ascii=False),
        "meta_tags_json": json.dumps(item.get("meta_tags") or [], ensure_ascii=False),
        "rating_json": json.dumps(rating, ensure_ascii=False),
        "collection_json": json.dumps(item.get("collection") or {}, ensure_ascii=False),
        "raw_json": json.dumps(item, ensure_ascii=False),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    columns = ",".join(payload.keys())
    placeholders = ",".join(["?"] * len(payload))
    updates = ",".join([f"{k}=excluded.{k}" for k in payload.keys() if k != "id"])

    conn.execute(
        f"INSERT INTO anime ({columns}) VALUES ({placeholders}) "
        f"ON CONFLICT(id) DO UPDATE SET {updates}",
        list(payload.values()),
    )

    conn.execute("DELETE FROM anime_tag WHERE anime_id = ?", (item.get("id"),))
    tags = item.get("tags") or []
    if not tags:
        return

    tag_cache: Dict[str, int] = {}
    for tag in tags:
        name = tag.get("name")
        if not name:
            continue
        if name not in tag_cache:
            conn.execute("INSERT OR IGNORE INTO tag(name) VALUES (?)", (name,))
            row = conn.execute("SELECT id FROM tag WHERE name = ?", (name,)).fetchone()
            tag_cache[name] = row["id"]
        conn.execute(
            "INSERT OR REPLACE INTO anime_tag(anime_id, tag_id, tag_count) VALUES (?, ?, ?)",
            (item.get("id"), tag_cache[name], tag.get("count")),
        )


def run_sync(full: bool = False) -> Tuple[bool, str]:
    limit = min(max(settings.sync_page_size, 1), 50)
    max_pages = None if full else max(settings.sync_recent_pages, 1)
    client = httpx.Client(base_url=settings.bangumi_api_base, headers=_headers(), timeout=30.0)
    conn = get_conn()

    try:
        page = 0
        offset = 0
        total_saved = 0
        while True:
            if max_pages is not None and page >= max_pages:
                break

            resp = client.get(
                "/v0/subjects",
                params={"type": 2, "limit": limit, "offset": offset},
            )
            if resp.status_code != 200:
                return False, f"bangumi api error: {resp.status_code} {resp.text}"

            data = resp.json() or {}
            total = data.get("total")
            items = data.get("data") or []
            if not items:
                break

            with conn:
                for item in items:
                    _upsert_anime(conn, item)
                    total_saved += 1

            page += 1
            offset += limit

            if isinstance(total, int) and offset >= total:
                break

        conn.execute(
            "INSERT OR REPLACE INTO sync_state(key, value) VALUES (?, ?)",
            ("last_sync_at", datetime.now(timezone.utc).isoformat()),
        )
        conn.execute(
            "INSERT OR REPLACE INTO sync_state(key, value) VALUES (?, ?)",
            ("last_sync_pages", str(page)),
        )
        if "total" in locals() and isinstance(total, int):
            conn.execute(
                "INSERT OR REPLACE INTO sync_state(key, value) VALUES (?, ?)",
                ("last_sync_total", str(total)),
            )
        conn.commit()
        mode = "full" if full else "recent"
        return True, f"sync {mode} complete, pages={page}, scanned={total_saved}"
    except Exception as exc:
        return False, f"sync failed: {exc}"
    finally:
        conn.close()
        client.close()
