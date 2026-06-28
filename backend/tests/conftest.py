"""Pytest configuration for Just4Tech backend tests."""

import os
import sys
import pytest
from pathlib import Path

# Make backend importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Ensure test API key is set
os.environ.setdefault("API_KEY", "test-api-key-for-testing")

# Use in-memory database for tests
os.environ["DB_PATH"] = ":memory:"


@pytest.fixture(scope="session")
def _app():
    """Create a FastAPI app for testing (session-scoped)."""
    from main import app
    return app


@pytest.fixture
def app(_app):
    """Per-test app with fresh DB."""
    from database import init_db
    init_db()
    # Clear caches and sessions
    import auth
    auth.SESSIONS.clear()
    import cache
    cache._cache.clear()
    # Reload API_KEY from env (it gets set once at import time)
    import config as _cfg
    _cfg.API_KEY = _cfg.load_api_key()
    return _app


@pytest.fixture
def client(app):
    """Test client using FastAPI TestClient."""
    from fastapi.testclient import TestClient
    return TestClient(app)
