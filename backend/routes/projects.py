"""Projects routes."""

from fastapi import APIRouter, Request, HTTPException

from database import get_db

router = APIRouter(tags=["projects"])


@router.get("/api/projects")
async def list_projects(request: Request):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM posts WHERE category='Project' AND status='active' "
        "ORDER BY created_at DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.get("/api/projects/{project_id}")
async def get_project(project_id: int):
    conn = get_db()
    project = conn.execute(
        "SELECT * FROM posts WHERE id = ? AND category='Project'", (project_id,)
    ).fetchone()
    conn.close()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return dict(project)
