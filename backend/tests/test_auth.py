"""Tests for authentication: API key, sessions, password hashing."""

import pytest
import os
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from auth import (
    require_api_key, check_session, create_session, destroy_session,
    update_session_username, hash_password, verify_password,
    check_rate_limit,
)
from config import API_KEY


class TestPasswordHashing:
    """Password hashing and verification."""

    def test_hash_and_verify_bcrypt(self):
        pw = "mysecretpassword"
        hashed = hash_password(pw)
        assert hashed.startswith("$2b$") or hashed.startswith("$2a$")
        assert verify_password(pw, hashed)
        assert not verify_password("wrongpassword", hashed)

    def test_verify_legacy_sha256_salted(self):
        pw = "oldpassword"
        import hashlib
        salt = "deadbeef" * 4
        h = hashlib.sha256((salt + pw).encode()).hexdigest()
        stored = f"sha256${salt}${h}"
        assert verify_password(pw, stored)
        assert not verify_password("wrong", stored)

    def test_verify_legacy_sha256_unsalted(self):
        import hashlib
        pw = "ancient"
        stored = hashlib.sha256(pw.encode()).hexdigest()
        assert verify_password(pw, stored)
        assert not verify_password("wrong", stored)


class TestSessionManagement:
    """Session create, check, destroy."""

    def test_create_and_check_session(self):
        token, expires = create_session("admin")
        assert token
        assert expires > datetime.now()

        mock_request = MagicMock()
        mock_request.cookies.get.return_value = token
        assert check_session(mock_request) == "admin"

    def test_expired_session(self):
        import auth
        token, _ = create_session("admin")
        # Manually expire the session
        auth.SESSIONS[token]["expires_at"] = datetime.now() - timedelta(seconds=1)

        mock_request = MagicMock()
        mock_request.cookies.get.return_value = token
        assert check_session(mock_request) is None
        assert token not in auth.SESSIONS

    def test_destroy_session(self):
        token, _ = create_session("admin")
        destroy_session(token)

        mock_request = MagicMock()
        mock_request.cookies.get.return_value = token
        assert check_session(mock_request) is None

    def test_update_session_username(self):
        token, _ = create_session("admin")
        update_session_username(token, "new_admin")

        mock_request = MagicMock()
        mock_request.cookies.get.return_value = token
        assert check_session(mock_request) == "new_admin"


class TestAPIKeyAuth:
    """API key authentication."""

    def test_valid_api_key(self):
        mock_request = MagicMock()
        mock_request.headers.get.return_value = API_KEY
        assert require_api_key(mock_request) is True

    def test_invalid_api_key(self):
        mock_request = MagicMock()
        mock_request.headers.get.return_value = "wrong-key"
        assert require_api_key(mock_request) is False

    def test_missing_api_key(self):
        mock_request = MagicMock()
        mock_request.headers.get.return_value = ""
        assert require_api_key(mock_request) is False


class TestRateLimiting:
    """Rate limiting for login endpoint."""

    def test_allows_first_requests(self):
        for i in range(5):
            assert check_rate_limit("test:127.0.0.1", 5, 60)

    def test_blocks_after_limit(self):
        for i in range(5):
            assert check_rate_limit("test:127.0.0.2", 5, 60)
        assert not check_rate_limit("test:127.0.0.2", 5, 60)

    def test_different_keys_independent(self):
        for i in range(5):
            assert check_rate_limit("test:127.0.0.3", 5, 60)
        # Different key should not be blocked
        assert check_rate_limit("test:127.0.0.4", 5, 60)


# ── Integration tests ──────────────────────────────────────────

def test_session_status_unauthenticated(client):
    resp = client.get("/api/admin/session-status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["authenticated"] is False
    assert data["user"] is None


def test_login_invalid_credentials(client):
    resp = client.post(
        "/api/admin/login",
        json={"username": "nobody", "password": "wrong"},
    )
    assert resp.status_code == 401
    data = resp.json()
    assert data["ok"] is False


def test_logout(client):
    resp = client.post("/api/admin/logout")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True
