from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..schemas import AnimeDetail, AnimeSearchResponse, SyncStatus
from ..services.search import get_anime_detail, search_anime
from ..services.sync import run_sync

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/anime/search", response_model=AnimeSearchResponse)
def anime_search(
    q: Optional[str] = Query(None, description="keyword"),
    tags: Optional[List[str]] = Query(None, description="tag filters"),
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    total, items = search_anime(q, tags, limit, offset)
    return {"total": total, "items": items}


@router.get("/anime/{anime_id}", response_model=AnimeDetail)
def anime_detail(anime_id: int):
    data = get_anime_detail(anime_id)
    if not data:
        raise HTTPException(status_code=404, detail="Not found")
    return data


@router.post("/sync/run", response_model=SyncStatus)
def sync_run():
    ok, msg = run_sync()
    return {"status": "ok" if ok else "error", "message": msg}
