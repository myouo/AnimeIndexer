from pydantic import BaseModel
from typing import List, Optional


class AnimeBase(BaseModel):
    id: int
    title: str
    title_original: Optional[str] = None
    author: Optional[str] = None
    description: Optional[str] = None
    score: Optional[float] = None
    cover_url: Optional[str] = None
    air_date: Optional[str] = None


class AnimeDetail(AnimeBase):
    tags: List[str] = []


class AnimeSearchResponse(BaseModel):
    total: int
    items: List[AnimeBase]


class SyncStatus(BaseModel):
    status: str
    message: str
