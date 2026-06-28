"""Software / AI Tools routes (public + admin)."""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from database import get_db
from auth import check_session

router = APIRouter(tags=["software"])


@router.get("/api/software")
async def list_software():
    conn = get_db()
    items = conn.execute(
        "SELECT * FROM posts WHERE category='AI Tool' AND status='active' "
        "ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(s) for s in items]


@router.get("/api/software/{sw_id}")
async def get_software(sw_id: int):
    conn = get_db()
    sw = conn.execute(
        "SELECT * FROM posts WHERE id = ? AND category='AI Tool'", (sw_id,)
    ).fetchone()
    conn.close()
    if not sw:
        raise HTTPException(status_code=404, detail="Tool not found")
    return dict(sw)


@router.get("/api/software/slug/{slug}")
async def get_software_by_slug(slug: str):
    conn = get_db()
    sw = conn.execute(
        "SELECT * FROM posts WHERE slug = ? AND category='AI Tool'", (slug,)
    ).fetchone()
    conn.close()
    if not sw:
        raise HTTPException(status_code=404, detail="Tool not found")
    return dict(sw)
