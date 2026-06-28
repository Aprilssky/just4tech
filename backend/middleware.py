"""HTTP middleware — page view tracking, etc."""

import logging
from datetime import date

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from database import get_db

logger = logging.getLogger("just4tech.middleware")


class PageViewMiddleware(BaseHTTPMiddleware):
    """Track page views (excluding admin, API, and static paths)."""

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.method == "GET" and not request.url.path.startswith(
            ("/admin", "/api", "/static")
        ):
            today = date.today().isoformat()
            path = request.url.path
            conn = get_db()
            try:
                conn.execute(
                    "INSERT INTO page_views (path, date, count) VALUES (?, ?, 1) "
                    "ON CONFLICT(path, date) DO UPDATE SET count = count + 1",
                    (path, today),
                )
                conn.commit()
            except Exception:
                logger.warning("Failed to track page view for %s", path, exc_info=True)
            finally:
                conn.close()
        return response
