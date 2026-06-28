"""Tests for icon proxy, RSS, sitemap, and other routes."""

import hashlib
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from routes.icon_proxy import _rewrite_icon_url, _guess_mime


class TestIconURLRewriting:
    """URL rewriter for blocked icon services."""

    def test_favicon_im_rewrite(self):
        url = "https://favicon.im/example.com"
        result = _rewrite_icon_url(url)
        assert result == "https://www.google.com/s2/favicons?domain=example.com&sz=64"

    def test_favicon_im_with_extra_path(self):
        url = "http://favicon.im/github.com/some/path"
        result = _rewrite_icon_url(url)
        assert result == "https://www.google.com/s2/favicons?domain=github.com&sz=64"

    def test_non_favicon_unchanged(self):
        url = "https://example.com/icon.png"
        result = _rewrite_icon_url(url)
        assert result == url


class TestMimeGuessing:
    """MIME type from file extension."""

    def test_png(self):
        assert _guess_mime("icon.png") == "image/png"
        assert _guess_mime("/path/to/file.PNG") == "image/png"

    def test_svg(self):
        assert _guess_mime("logo.svg") == "image/svg+xml"

    def test_unknown(self):
        assert _guess_mime("file.xyz") == "image/png"  # default


class TestRSSFeed:
    """RSS feed endpoint."""

    def test_rss_feed_empty(self, client):
        resp = client.get("/rss.xml")
        assert resp.status_code == 200
        assert "application/rss+xml" in resp.headers["content-type"]
        assert "<rss" in resp.text

    def test_rss_feed_with_posts(self, client):
        from database import get_db
        conn = get_db()
        conn.execute(
            "INSERT INTO posts (slug, title, content, status, excerpt) VALUES (?, ?, ?, ?, ?)",
            ("rss-post", "RSS Test Post", "Content here", "active", "A great excerpt"),
        )
        conn.commit()
        conn.close()

        resp = client.get("/rss.xml")
        assert resp.status_code == 200
        content = resp.text
        assert "<title>RSS Test Post</title>" in content
        assert "A great excerpt" in content


class TestSitemap:
    """Sitemap endpoint."""

    def test_sitemap_basic(self, client):
        resp = client.get("/sitemap.xml")
        assert resp.status_code == 200
        assert "application/xml" in resp.headers["content-type"]
        content = resp.text
        assert "just4.tech" in content
        assert "<urlset" in content


class TestProjects:
    """Projects API."""

    def test_projects_empty(self, client):
        resp = client.get("/api/projects")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_projects_with_data(self, client):
        from database import get_db
        conn = get_db()
        conn.execute(
            "INSERT INTO posts (slug, title, content, status, category) VALUES (?, ?, ?, ?, ?)",
            ("my-proj", "My Project", "Details", "active", "Project"),
        )
        conn.close()

        resp = client.get("/api/projects")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "My Project"


class TestContact:
    """Contact form submission."""

    def test_submit_contact(self, client):
        resp = client.post(
            "/api/contact",
            json={
                "name": "Test User",
                "email": "test@example.com",
                "subject": "general",
                "message": "Hello!",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True

    def test_contact_messages_require_auth(self, client):
        resp = client.get("/api/admin/contact-messages")
        assert resp.status_code == 401
