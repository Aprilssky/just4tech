"""RSS feed and sitemap generation."""

import logging
from datetime import date, timezone, datetime
from email.utils import format_datetime
from xml.sax.saxutils import escape as xml_escape

from fastapi import APIRouter
from fastapi.responses import Response

from database import get_db
from cache import cached
from config import RSS_CACHE_TTL, SITEMAP_CACHE_TTL

logger = logging.getLogger("just4tech.routes.sitemap")
router = APIRouter(tags=["sitemap"])


@router.get("/rss.xml", response_class=Response)
@cached("rss_feed", ttl_seconds=RSS_CACHE_TTL)
async def rss_feed():
    conn = get_db()
    posts = conn.execute(
        "SELECT * FROM posts WHERE status='active' ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    conn.close()

    latest_date = None
    items = []
    for p in posts:
        raw = p["created_at"] or ""
        if raw:
            try:
                dt = datetime.strptime(raw[:19], "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.utc
                )
                pd = format_datetime(dt, usegmt=True)
                if latest_date is None or dt > latest_date:
                    latest_date = dt
            except Exception:
                pd = raw[:19]
        else:
            pd = str(date.today())

        title = xml_escape(p["title"] or "")
        excerpt = xml_escape((p["excerpt"] or "")[:500])
        category = xml_escape(p["category"] or "")
        slug = xml_escape(p["slug"] or "")

        items.append(
            f"<item><title>{title}</title>"
            f"<link>https://just4.tech/blog/{slug}</link>"
            f"<guid>https://just4.tech/blog/{slug}</guid>"
            f"<description><![CDATA[{excerpt}]]></description>"
            f"<pubDate>{pd}</pubDate>"
            f"<category>{category}</category></item>"
        )

    build_date = (
        format_datetime(latest_date, usegmt=True)
        if latest_date
        else format_datetime(datetime.now(timezone.utc), usegmt=True)
    )

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append(
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel>'
    )
    lines.append(
        "<title>Just4Tech Blog</title>"
        "<link>https://just4.tech/blog</link>"
    )
    lines.append(
        "<description>Indie dev stories, tutorials, and tool reviews</description>"
    )
    lines.append(f"<lastBuildDate>{build_date}</lastBuildDate>")
    lines.append("<language>en</language>")
    lines.append(
        '<atom:link href="https://just4.tech/rss.xml" rel="self" '
        'type="application/rss+xml"/>'
    )
    lines.extend(items)
    lines.append("</channel></rss>")
    return Response(content="\n".join(lines), media_type="application/rss+xml")


@router.get("/sitemap.xml", response_class=Response)
@cached("sitemap", ttl_seconds=SITEMAP_CACHE_TTL)
async def sitemap():
    conn = get_db()
    posts = conn.execute(
        "SELECT slug, updated_at FROM posts WHERE status='active' "
        "AND category NOT IN ('AI Tool','Project','Indie Dev','Site') "
        "ORDER BY updated_at DESC"
    ).fetchall()
    software = conn.execute(
        "SELECT slug, updated_at FROM posts WHERE status='active' "
        "AND category='AI Tool' ORDER BY updated_at DESC"
    ).fetchall()
    projects = conn.execute(
        "SELECT slug, updated_at FROM posts WHERE status='active' "
        "AND category='Project' ORDER BY updated_at DESC"
    ).fetchall()
    indie_devs = conn.execute(
        "SELECT slug, updated_at FROM posts WHERE status='active' "
        "AND category='Indie Dev' ORDER BY updated_at DESC"
    ).fetchall()
    sites_posts = conn.execute(
        "SELECT slug, updated_at FROM posts WHERE status='active' "
        "AND category='Site' ORDER BY updated_at DESC"
    ).fetchall()
    conn.close()

    today = date.today().isoformat()
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    static_pages = [
        ("/", "1.0", "daily"),
        ("/blog", "0.8", "weekly"),
        ("/aitools", "0.8", "weekly"),
        ("/projects", "0.7", "weekly"),
        ("/indie-devs", "0.6", "monthly"),
        ("/tutorials", "0.7", "weekly"),
        ("/sites", "0.6", "monthly"),
        ("/about", "0.6", "monthly"),
        ("/contact", "0.5", "monthly"),
        ("/privacy", "0.3", "monthly"),
        ("/terms", "0.3", "monthly"),
    ]
    for page, priority, freq in static_pages:
        lines.append(
            f"  <url><loc>https://just4.tech{page}</loc>"
            f"<lastmod>{today}</lastmod>"
            f"<changefreq>{freq}</changefreq>"
            f"<priority>{priority}</priority></url>"
        )

    def url_entry(loc, slug, updated, priority, freq="weekly"):
        upd = (updated or "")[:10] or today
        s = xml_escape(slug)
        lines.append(
            f"  <url><loc>{loc}/{s}</loc>"
            f"<lastmod>{upd}</lastmod>"
            f"<changefreq>{freq}</changefreq>"
            f"<priority>{priority}</priority></url>"
        )

    for p in posts:
        url_entry("https://just4.tech/blog", p["slug"], p["updated_at"], "0.7")
    for s in software:
        url_entry("https://just4.tech/aitools", s["slug"], s["updated_at"], "0.6", "monthly")
    for p in projects:
        url_entry("https://just4.tech/projects", p["slug"], p["updated_at"], "0.6", "monthly")
    for d in indie_devs:
        url_entry("https://just4.tech/blog", d["slug"], d["updated_at"], "0.5")
    for s in sites_posts:
        url_entry("https://just4.tech/sites", s["slug"], s["updated_at"], "0.6")

    lines.append("</urlset>")
    return Response(content="\n".join(lines), media_type="application/xml")
