"""Routes package — aggregates all API routers."""

from .posts import router as posts_router
from .admin import router as admin_router
from .pages import router as pages_router
from .media import router as media_router
from .contact import router as contact_router
from .software import router as software_router
from .projects import router as projects_router
from .content import router as content_router
from .icon_proxy import router as icon_proxy_router
from .sitemap import router as sitemap_router

__all__ = [
    "posts_router",
    "admin_router",
    "pages_router",
    "media_router",
    "contact_router",
    "software_router",
    "projects_router",
    "content_router",
    "icon_proxy_router",
    "sitemap_router",
]
