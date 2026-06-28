"""Just4Tech Backend — modular FastAPI application.

Organized into:
- config.py       — all settings, no hardcoded paths
- auth.py         — API key auth, session management, password hashing, rate limiting
- cache.py        — in-memory TTL cache
- database.py     — SQLite connection + schema
- middleware.py   — HTTP middleware (page view tracking)
- routes/         — API route modules (posts, admin, pages, media, contact, etc.)
"""

import asyncio
import logging
import os as _os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import (
    CORS_ORIGINS, CORS_ORIGIN_REGEX, SERVER_HOST, SERVER_PORT,
    STATIC_DIR, UPLOAD_DIR, ICON_CACHE_DIR, API_KEY,
)
from database import init_db
from middleware import PageViewMiddleware

# ── Logging setup ──────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if _os.environ.get("DEBUG") else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("just4tech")

# ── App creation ───────────────────────────────────────────────
app = FastAPI(title="AI Tool Hub Admin")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Page view tracking
app.add_middleware(PageViewMiddleware)

# Static file serving
for dir_path, mount_path in [
    (STATIC_DIR, "/static"),
    (UPLOAD_DIR, "/uploads"),
    (ICON_CACHE_DIR, "/static/icon-cache"),
]:
    dir_path = Path(dir_path)
    dir_path.mkdir(parents=True, exist_ok=True)
    app.mount(mount_path, StaticFiles(directory=str(dir_path)), name=mount_path.lstrip("/"))

# ── Register routes ────────────────────────────────────────────
from routes import (
    posts_router, admin_router, pages_router, media_router,
    contact_router, software_router, projects_router,
    content_router, icon_proxy_router, sitemap_router,
)

routers = [
    posts_router, admin_router, pages_router, media_router,
    contact_router, software_router, projects_router,
    content_router, icon_proxy_router, sitemap_router,
]
for router in routers:
    app.include_router(router)


# ── Startup ────────────────────────────────────────────────────
@app.on_event("startup")
async def startup():
    init_db()
    from migrations import run_migrations
    run_migrations()
    logger.info("API_KEY loaded (%d chars)", len(API_KEY))
    # Pre-warm icon cache in background
    from routes.icon_proxy import prewarm_icon_cache
    asyncio.create_task(prewarm_icon_cache())


# ── Entry point ────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
