"""Posts CRUD routes."""

import logging

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse

from database import get_db
from auth import check_session, require_api_key, api_key_required
from cache import invalidate_cache

logger = logging.getLogger("just4tech.routes.posts")
router = APIRouter(tags=["posts"])


@router.get("/api/posts")
async def list_posts(request: Request, status: str = "", page: int = 0, limit: int = 20):
    conn = get_db()
    user = check_session(request)

    base_query = "FROM posts"
    params: list = []
    if status:
        if status == "all":
            base_query += " ORDER BY created_at DESC"
        else:
            base_query += " WHERE status = ? ORDER BY created_at DESC"
            params.append(status)
    elif user or require_api_key(request):
        base_query += " ORDER BY created_at DESC"
    else:
        base_query += " WHERE status = 'active' ORDER BY created_at DESC"

    if page > 0:
        offset = (page - 1) * limit
        count_row = conn.execute(
            f"SELECT COUNT(*) as cnt {base_query}", params
        ).fetchone()
        total = count_row["cnt"]
        rows = conn.execute(
            f"SELECT * {base_query} LIMIT ? OFFSET ?", params + [limit, offset]
        ).fetchall()
        conn.close()
        return {"posts": [dict(r) for r in rows], "total": total, "page": page, "limit": limit}
    else:
        rows = conn.execute(f"SELECT * {base_query}", params).fetchall()
        conn.close()
        return [dict(r) for r in rows]


@router.get("/api/posts/{post_id}")
async def get_post(post_id: int, request: Request):
    conn = get_db()
    user = check_session(request)
    if user or require_api_key(request):
        post = conn.execute("SELECT * FROM posts WHERE id = ?", (post_id,)).fetchone()
    else:
        post = conn.execute(
            "SELECT * FROM posts WHERE id = ? AND status = 'active'", (post_id,)
        ).fetchone()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return dict(post)


@router.get("/api/posts/slug/{slug}")
async def get_post_by_slug(slug: str, request: Request):
    conn = get_db()
    user = check_session(request)
    if user or require_api_key(request):
        post = conn.execute("SELECT * FROM posts WHERE slug = ?", (slug,)).fetchone()
    else:
        post = conn.execute(
            "SELECT * FROM posts WHERE slug = ? AND status = 'active'", (slug,)
        ).fetchone()
    conn.close()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return dict(post)


@router.post("/api/posts")
async def create_post(request: Request):
    user = check_session(request)
    if not (user or require_api_key(request)):
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    conn = get_db()
    conn.execute(
        """INSERT INTO posts (slug, title, content, category, excerpt, tags, author,
           status, cover_image, icon, subtitle, external_url)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            data["slug"], data["title"], data["content"],
            data.get("category", "review"), data.get("excerpt", ""),
            data.get("tags", ""), data.get("author", "AI Tool Hub Team"),
            data.get("status", "draft"), data.get("cover_image", ""),
            data.get("icon", ""), data.get("subtitle", ""),
            data.get("external_url", ""),
        ),
    )
    conn.commit()
    post_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    conn.close()
    invalidate_cache("rss_feed", "sitemap")
    logger.info("Post created: id=%d slug=%s", post_id, data.get("slug", ""))
    return {"ok": True, "id": post_id}


@router.put("/api/posts/{post_id}")
async def update_post(post_id: int, request: Request):
    user = check_session(request)
    if not (user or require_api_key(request)):
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    conn = get_db()
    existing = conn.execute(
        "SELECT slug, title, content, category, excerpt, tags, author, "
        "status, cover_image, icon, subtitle, external_url FROM posts WHERE id=?",
        (post_id,),
    ).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")
    conn.execute(
        """UPDATE posts SET slug=?, title=?, content=?, category=?, excerpt=?,
           tags=?, author=?, status=?, cover_image=?, icon=?, subtitle=?,
           external_url=?, updated_at=CURRENT_TIMESTAMP WHERE id=?""",
        (
            data.get("slug", existing["slug"]),
            data.get("title", existing["title"]),
            data.get("content", existing["content"]),
            data.get("category", existing["category"]),
            data.get("excerpt", existing["excerpt"] or ""),
            data.get("tags", existing["tags"] or ""),
            data.get("author", existing["author"] or "AI Tool Hub Team"),
            data.get("status", existing["status"] or "draft"),
            data.get("cover_image", existing["cover_image"] or ""),
            data.get("icon", existing["icon"] or ""),
            data.get("subtitle", existing["subtitle"] or ""),
            data.get("external_url", existing["external_url"] or ""),
            post_id,
        ),
    )
    conn.commit()
    conn.close()
    invalidate_cache("rss_feed", "sitemap")
    logger.info("Post updated: id=%d", post_id)
    return {"ok": True}


@router.delete("/api/posts/{post_id}")
async def delete_post(post_id: int, request: Request):
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Admin session required to delete posts")
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    invalidate_cache("rss_feed", "sitemap")
    logger.info("Post deleted: id=%d", post_id)
    return {"ok": True}


# ── Slug-based operations ─────────────────────────────────────

@router.put("/api/posts/slug/{slug}")
async def update_post_by_slug(slug: str, request: Request):
    user = check_session(request)
    if not (user or require_api_key(request)):
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    conn = get_db()
    existing = conn.execute("SELECT id FROM posts WHERE slug=?", (slug,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Post not found")

    allowed_fields = [
        "title", "content", "category", "excerpt", "tags", "author",
        "status", "cover_image", "slug", "icon", "subtitle", "external_url",
    ]
    fields = []
    values = []
    for f in allowed_fields:
        if f in data:
            fields.append(f"{f}=?")
            values.append(data[f])
    if not fields:
        conn.close()
        return {"ok": False, "error": "No fields to update"}
    values.append(slug)
    conn.execute(
        f"UPDATE posts SET {', '.join(fields)}, updated_at=CURRENT_TIMESTAMP WHERE slug=?",
        values,
    )
    conn.commit()
    conn.close()
    invalidate_cache("rss_feed", "sitemap")
    logger.info("Post updated by slug: %s", slug)
    return {"ok": True}


@router.delete("/api/posts/slug/{slug}")
async def delete_post_by_slug(slug: str, request: Request):
    user = check_session(request)
    if not (user or require_api_key(request)):
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    conn.execute("DELETE FROM posts WHERE slug=?", (slug,))
    conn.commit()
    conn.close()
    invalidate_cache("rss_feed", "sitemap")
    logger.info("Post deleted by slug: %s", slug)
    return {"ok": True, "slug": slug}
