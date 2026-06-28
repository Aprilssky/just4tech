"""Content blocks API — editable page content sections."""

from fastapi import APIRouter, Request, HTTPException

from database import get_db
from auth import check_session

router = APIRouter(tags=["content"])


@router.get("/api/content/pages/list")
async def list_content_pages():
    conn = get_db()
    rows = conn.execute(
        "SELECT DISTINCT page_path FROM content_blocks ORDER BY page_path"
    ).fetchall()
    conn.close()
    return {"pages": [r["page_path"] for r in rows]}


@router.get("/api/content/{page_path:path}")
async def get_content(page_path: str):
    if not page_path:
        page_path = "/"
    conn = get_db()
    blocks = conn.execute(
        "SELECT block_key, content, content_type FROM content_blocks WHERE page_path = ?",
        (page_path,),
    ).fetchall()
    conn.close()
    return {
        "blocks": [
            {"block_key": b["block_key"], "content": b["content"],
             "content_type": b["content_type"]}
            for b in blocks
        ]
    }


@router.put("/api/content/{page_path:path}/{block_key}")
async def update_content(page_path: str, block_key: str, request: Request):
    if not page_path:
        page_path = "/"
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    content = data.get("content", "")
    content_type = data.get("content_type", "text")
    conn = get_db()
    conn.execute(
        """INSERT INTO content_blocks (page_path, block_key, content, content_type, updated_at)
           VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
           ON CONFLICT(page_path, block_key) DO UPDATE SET
               content = excluded.content,
               content_type = excluded.content_type,
               updated_at = CURRENT_TIMESTAMP""",
        (page_path, block_key, content, content_type),
    )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.post("/api/content/{page_path:path}/bulk")
async def bulk_update_content(page_path: str, request: Request):
    if not page_path:
        page_path = "/"
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    data = await request.json()
    blocks = data.get("blocks", [])
    conn = get_db()
    for block in blocks:
        conn.execute(
            """INSERT INTO content_blocks (page_path, block_key, content, content_type, updated_at)
               VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(page_path, block_key) DO UPDATE SET
                   content = excluded.content,
                   content_type = excluded.content_type,
                   updated_at = CURRENT_TIMESTAMP""",
            (page_path, block["block_key"],
             block.get("content", ""), block.get("content_type", "text")),
        )
    conn.commit()
    conn.close()
    return {"ok": True}


@router.delete("/api/content/{page_path:path}/{block_key}")
async def delete_content(page_path: str, block_key: str, request: Request):
    if not page_path:
        page_path = "/"
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    conn = get_db()
    conn.execute(
        "DELETE FROM content_blocks WHERE page_path = ? AND block_key = ?",
        (page_path, block_key),
    )
    conn.commit()
    conn.close()
    return {"ok": True}
