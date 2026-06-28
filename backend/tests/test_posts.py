"""Tests for posts CRUD API."""

import pytest
from fastapi.testclient import TestClient


# Helper to create an admin user and get auth cookies
def _create_admin(client: TestClient) -> dict:
    """Create an admin user in the database and return credentials."""
    from database import get_db
    from auth import hash_password
    conn = get_db()
    conn.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        ("admin", hash_password("admin123")),
    )
    conn.commit()
    conn.close()
    return {"username": "admin", "password": "admin123"}


def _login(client: TestClient) -> str:
    """Login as admin and return session cookie."""
    _create_admin(client)
    resp = client.post("/api/admin/login", json={"username": "admin", "password": "admin123"})
    assert resp.status_code == 200
    cookie = resp.headers.get("set-cookie", "")
    return cookie


class TestPostsPublic:
    """Public post listing endpoints."""

    def test_list_posts_empty(self, client):
        resp = client.get("/api/posts")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_posts_with_drafts_hidden(self, client):
        from database import get_db
        conn = get_db()
        conn.execute(
            "INSERT INTO posts (slug, title, content, status) VALUES (?, ?, ?, ?)",
            ("draft-post", "Draft", "Content", "draft"),
        )
        conn.commit()
        conn.close()

        resp = client.get("/api/posts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 0  # Drafts hidden from public

    def test_list_posts_active_visible(self, client):
        from database import get_db
        conn = get_db()
        conn.execute(
            "INSERT INTO posts (slug, title, content, status) VALUES (?, ?, ?, ?)",
            ("active-post", "Active Post", "Hello world", "active"),
        )
        conn.commit()
        conn.close()

        resp = client.get("/api/posts")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["title"] == "Active Post"


class TestPostsAuthenticated:
    """Posts CRUD with admin session."""

    def test_create_post(self, client):
        cookie = _login(client)

        resp = client.post(
            "/api/posts",
            json={"slug": "test-post", "title": "Test", "content": "Body"},
            headers={"Cookie": cookie},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["ok"] is True
        assert data["id"] > 0

    def test_get_post_by_id(self, client):
        cookie = _login(client)

        # Create first
        client.post(
            "/api/posts",
            json={"slug": "my-post", "title": "My Post", "content": "Test content"},
            headers={"Cookie": cookie},
        )

        # Get by ID
        resp = client.get("/api/posts/1")
        assert resp.status_code == 200
        data = resp.json()
        assert data["slug"] == "my-post"
        assert data["title"] == "My Post"

    def test_get_post_by_slug(self, client):
        cookie = _login(client)

        client.post(
            "/api/posts",
            json={"slug": "slug-post", "title": "Slug", "content": "X"},
            headers={"Cookie": cookie},
        )

        resp = client.get("/api/posts/slug/slug-post")
        assert resp.status_code == 200
        assert resp.json()["title"] == "Slug"

    def test_update_post(self, client):
        cookie = _login(client)

        client.post(
            "/api/posts",
            json={"slug": "upd", "title": "Old", "content": "Old"},
            headers={"Cookie": cookie},
        )

        resp = client.put(
            "/api/posts/1",
            json={"title": "New Title"},
            headers={"Cookie": cookie},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] is True

        # Verify updated
        resp = client.get("/api/posts/1")
        assert resp.json()["title"] == "New Title"

    def test_delete_post(self, client):
        cookie = _login(client)

        client.post(
            "/api/posts",
            json={"slug": "del", "title": "Delete Me", "content": "X"},
            headers={"Cookie": cookie},
        )

        resp = client.delete("/api/posts/1", headers={"Cookie": cookie})
        assert resp.status_code == 200

        # Should be gone
        resp = client.get("/api/posts/1")
        assert resp.status_code == 404

    def test_delete_post_requires_session(self, client):
        """Delete requires admin session, not just API key."""
        resp = client.delete(
            "/api/posts/1",
            headers={"X-API-Key": "test-api-key-for-testing"},
        )
        assert resp.status_code == 401

    def test_pagination(self, client):
        from database import get_db
        conn = get_db()
        for i in range(5):
            conn.execute(
                "INSERT INTO posts (slug, title, content, status) VALUES (?, ?, ?, ?)",
                (f"post-{i}", f"Post {i}", f"Content {i}", "active"),
            )
        conn.commit()
        conn.close()

        resp = client.get("/api/posts?page=1&limit=2")
        data = resp.json()
        assert data["total"] == 5
        assert data["page"] == 1
        assert len(data["posts"]) == 2

    def test_create_post_with_api_key(self, client):
        resp = client.post(
            "/api/posts",
            json={"slug": "api-post", "title": "API", "content": "X"},
            headers={"X-API-Key": "test-api-key-for-testing"},
        )
        assert resp.status_code == 200
        assert resp.json()["ok"] is True
