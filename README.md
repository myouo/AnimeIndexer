# AnimeIndexer

Desktop anime indexer (Electron + React) with a local FastAPI backend and SQLite storage.

## Goals
- Tag-based filtering
- Detail view (title, images, summary, infobox, tags)
- Local search via backend API

## Repo layout
- `backend/` FastAPI + SQLite (data + sync)
- `frontend/` Electron + React renderer

## Backend (FastAPI)
- Entry: `backend/app/main.py`
- DB schema: `backend/schema.sql`
- Init DB: `python -m backend.app.init_db`

### .env
Create a `.env` file (see `.env.example`).
- `BANGUMI_ACCESS_TOKEN`
- `USER_AGENT` (must include your ID + app name)

### API contract (local)
- `GET /health`
- `GET /anime/search?q=keyword&tags=tag1&tags=tag2&limit=30&offset=0`
- `GET /anime/{id}`
- `POST /sync/run` (recent pages)
- `POST /sync/run?full=true` (full scan)

## Sync plan (Bangumi)
- Pull from `/v0/subjects?type=2` with pagination (`limit <= 50`).
- Filter out score < 3.0.
- Upsert into `anime`, `tag`, `anime_tag`.
- Store raw json + infobox/tags for extensible detail view.
- Incremental strategy: re-scan recent pages; full scan available for score refresh.

## Frontend (Electron)
- Main process: `frontend/app/electron/main.js`
- Preload: `frontend/app/electron/preload.js`
- Renderer: `frontend/app/renderer/src/`

## Next steps
- Implement the UI for tags and infobox display.
- Add background sync scheduling.
- Add image caching + lazy loading.
