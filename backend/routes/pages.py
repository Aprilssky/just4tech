"""Static pages routes."""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse

from database import get_db
from auth import check_session

router = APIRouter(tags=["pages"])


@router.get("/api/pages")
async def list_pages(request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    pages = conn.execute(
        "SELECT id, slug, title, meta_title, meta_description FROM site_pages ORDER BY slug"
    ).fetchall()
    conn.close()
    return [dict(p) for p in pages]


@router.get("/api/page/{slug}")
async def get_public_page(slug: str):
    conn = get_db()
    page = conn.execute("SELECT * FROM site_pages WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return dict(page)


@router.get("/api/pages/{page_id}")
async def get_page(page_id: int, request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    page = conn.execute("SELECT * FROM site_pages WHERE id = ?", (page_id,)).fetchone()
    conn.close()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return dict(page)


@router.put("/api/pages/{page_id}")
async def update_page(page_id: int, request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    conn = get_db()
    conn.execute(
        """UPDATE site_pages SET title=?, meta_title=?, meta_description=?,
           content=?, updated_at=CURRENT_TIMESTAMP WHERE id=?""",
        (
            data.get("title", ""),
            data.get("meta_title", ""),
            data.get("meta_description", ""),
            data.get("content", ""),
            page_id,
        ),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.get("/api/pages/list")
async def list_page_paths():
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT page_path FROM content_blocks ORDER BY page_path"
    ).fetchall()
    conn.close()
    return {"pages": [r["page_path"] for r in rows]}


# ── Public page rendering (server-side via Jinja2) ─────────────

from config import TEMPLATES_DIR
from jinja2 import Environment, FileSystemLoader

_jinja_env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)), autoescape=True)


def _render(template_name: str, **context) -> HTMLResponse:
    template = _jinja_env.get_template(template_name)
    return HTMLResponse(template.render(**context))


@router.get("/page/{slug}", response_class=HTMLResponse)
async def public_page(request: Request, slug: str):
    conn = get_db()
    page = conn.execute("SELECT * FROM site_pages WHERE slug = ?", (slug,)).fetchone()
    conn.close()
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    meta_title = page["meta_title"] or page["title"]
    meta_desc = page["meta_description"] or ""
    return _render("public/page.html", request=request, page=page,
                    meta_title=meta_title, meta_desc=meta_desc)
