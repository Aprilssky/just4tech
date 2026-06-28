"""Icon proxy: fetch, cache, and serve external tool icons."""

import re
import hashlib
import logging
from urllib.parse import unquote

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response, FileResponse

from config import (
    ICON_CACHE_DIR, ICON_MAX_SIZE, ICON_FETCH_TIMEOUT,
    ICON_CACHE_MAX_AGE, ICON_FETCH_HEADERS,
)
from database import get_db

logger = logging.getLogger("just4tech.routes.icon_proxy")
router = APIRouter(tags=["icon_proxy"])


def _rewrite_icon_url(url: str) -> str:
    """Rewrite known icon-service URLs to alternatives that don't block servers."""
    # favicon.im → Google favicon service (server-friendly)
    # Extract just the domain from favicon.im URLs
    m = re.match(r"https?://favicon\.im/([^/]+)", url)
    if m:
        domain = m.group(1).rstrip("/")
        return f"https://www.google.com/s2/favicons?domain={domain}&sz=64"
    return url


def _guess_mime(path: str) -> str:
    ext = path.rsplit(".", 1)[-1].lower() if "." in path else ""
    return {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "gif": "image/gif", "webp": "image/webp",
        "svg": "image/svg+xml", "ico": "image/x-icon",
    }.get(ext, "image/png")


@router.get("/api/icon-proxy")
async def icon_proxy(url: str = ""):
    """Proxy external icon URLs through our domain with disk caching."""
    if not url:
        raise HTTPException(status_code=400, detail="Missing `url` query parameter")

    remote_url = unquote(url)
    if not remote_url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="Only http/https URLs are allowed")

    cache_key = hashlib.sha256(remote_url.encode()).hexdigest()
    cache_path = ICON_CACHE_DIR / cache_key

    # Serve from disk cache if available
    if cache_path.exists():
        return FileResponse(
            str(cache_path),
            media_type=_guess_mime(cache_path.name),
            headers={"Cache-Control": f"public, max-age={ICON_CACHE_MAX_AGE}"},
        )

    fetch_url = _rewrite_icon_url(remote_url)

    try:
        async with httpx.AsyncClient(
            timeout=ICON_FETCH_TIMEOUT, headers=ICON_FETCH_HEADERS
        ) as client:
            resp = await client.get(fetch_url, follow_redirects=True)
            if resp.status_code != 200:
                raise HTTPException(
                    status_code=404,
                    detail=f"Remote icon returned {resp.status_code}",
                )
            body = resp.read()
            if len(body) > ICON_MAX_SIZE:
                raise HTTPException(
                    status_code=400, detail="Remote icon exceeds size limit"
                )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Failed to fetch remote icon")

    content_type = resp.headers.get("content-type", "image/png")

    # Write to disk cache
    ICON_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(body)
    logger.debug("Icon cached: %s → %s", remote_url[:60], cache_key[:12])

    return Response(
        content=body,
        media_type=content_type,
        headers={"Cache-Control": f"public, max-age={ICON_CACHE_MAX_AGE}"},
    )


# ── Startup pre-warm ──────────────────────────────────────────

async def prewarm_icon_cache():
    """Fetch all AI tool icons in the background and populate disk cache."""
    conn = get_db()
    tools = conn.execute(
        "SELECT icon FROM posts WHERE category='AI Tool' AND status='active' "
        "AND icon LIKE 'http%'"
    ).fetchall()
    conn.close()

    icons = [
        t["icon"].strip()
        for t in tools
        if t["icon"] and t["icon"].strip().startswith(("http://", "https://"))
    ]
    if not icons:
        return

    logger.info("Pre-warming %d tool icons...", len(icons))
    cached = 0
    for remote_url in icons:
        cache_key = hashlib.sha256(remote_url.encode()).hexdigest()
        cache_path = ICON_CACHE_DIR / cache_key
        if cache_path.exists():
            cached += 1
            continue
        try:
            fetch_url = _rewrite_icon_url(remote_url)
            async with httpx.AsyncClient(
                timeout=ICON_FETCH_TIMEOUT, headers=ICON_FETCH_HEADERS
            ) as client:
                resp = await client.get(fetch_url, follow_redirects=True)
                if resp.status_code == 200:
                    body = resp.read()
                    if len(body) <= ICON_MAX_SIZE:
                        ICON_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                        cache_path.write_bytes(body)
                        cached += 1
        except Exception:
            logger.debug("Icon prewarm failed for %s", remote_url[:60])
    logger.info("Icon pre-warm complete: %d/%d cached", cached, len(icons))
