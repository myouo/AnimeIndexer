from pydantic import BaseModel
from typing import Any, Dict, List, Optional


class AnimeBase(BaseModel):
    id: int
    title: str
    title_original: Optional[str] = None
    name_cn: Optional[str] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    description: Optional[str] = None
    score: Optional[float] = None
    rank: Optional[int] = None
    cover_url: Optional[str] = None
    date: Optional[str] = None
    platform: Optional[str] = None


class AnimeDetail(AnimeBase):
    tags: List[str] = []
    images: Optional[Dict[str, Any]] = None
    infobox: Optional[List[Dict[str, Any]]] = None
    meta_tags: Optional[List[str]] = None
    rating: Optional[Dict[str, Any]] = None
    collection: Optional[Dict[str, Any]] = None
    raw: Optional[Dict[str, Any]] = None


class AnimeSearchResponse(BaseModel):
    total: int
    items: List[AnimeBase]


class SyncStatus(BaseModel):
    status: str
    message: str
