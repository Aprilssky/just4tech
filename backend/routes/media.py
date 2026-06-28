"""Media upload, list, delete routes."""

import os as _os
import uuid as _uuid
import logging
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException, UploadFile
from fastapi.responses import JSONResponse

from auth import check_session
from config import UPLOAD_DIR, NGINX_UPLOAD_DIR, UPLOAD_MAX_SIZE, ALLOWED_UPLOAD_EXTS

logger = logging.getLogger("just4tech.routes.media")
router = APIRouter(tags=["media"])


@router.post("/api/admin/upload")
async def upload_media(request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    try:
        form = await request.form()
        file = form.get("file")
        if not file:
            return JSONResponse({"ok": False, "error": "No file provided"})

        filename = file.filename or "image.png"
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_UPLOAD_EXTS:
            return JSONResponse({"ok": False, "error": f"Invalid file type: {ext}"})

        contents = await file.read()
        if len(contents) > UPLOAD_MAX_SIZE:
            return JSONResponse({"ok": False, "error": "File too large (max 5MB)"})

        safe_name = _uuid.uuid4().hex[:12] + ext
        url = "/uploads/" + safe_name

        # Write to primary upload dir
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        (UPLOAD_DIR / safe_name).write_bytes(contents)

        # Also write to Nginx SPA upload dir (for production serving)
        nginx_path = Path(NGINX_UPLOAD_DIR)
        nginx_path.mkdir(parents=True, exist_ok=True)
        (nginx_path / safe_name).write_bytes(contents)

        logger.info("Media uploaded: %s (%d bytes)", safe_name, len(contents))
        return JSONResponse({"ok": True, "url": url})

    except Exception as e:
        logger.exception("Media upload failed")
        return JSONResponse({"ok": False, "error": str(e)})


@router.get("/api/admin/media")
async def list_media(request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    from datetime import datetime

    files = []
    if UPLOAD_DIR.exists():
        for fpath in sorted(UPLOAD_DIR.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
            if fpath.name == ".gitkeep":
                continue
            size = fpath.stat().st_size
            files.append({
                "filename": fpath.name,
                "url": "/uploads/" + fpath.name,
                "size": size,
                "size_display": (
                    f"{size/1024:.1f} KB" if size < 1024 * 1024
                    else f"{size/1024/1024:.1f} MB"
                ),
                "updated_at": datetime.fromtimestamp(fpath.stat().st_mtime).strftime(
                    "%Y-%m-%d %H:%M"
                ),
            })
    return {"files": files}


@router.delete("/api/admin/media/{filename:path}")
async def delete_media(filename: str, request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")

    for base_dir in [UPLOAD_DIR, Path(NGINX_UPLOAD_DIR)]:
        fpath = base_dir / filename
        if fpath.exists():
            fpath.unlink()
            logger.info("Media deleted: %s from %s", filename, base_dir)

    return {"ok": True}
