"""Pytest configuration for Just4Tech backend tests."""

import os
import sys
import tempfile
import pytest
from pathlib import Path

# Make backend importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

# Ensure test API key is set
os.environ.setdefault("API_KEY", "test-api-key-for-testing")

# Use a temp file database for tests (simpler than in-memory shared cache)
_db_file = tempfile.NamedTemporaryFile(suffix=".db", delete=False, prefix="test_just4tech_")
_db_path = _db_file.name
_db_file.close()
os.environ["DB_PATH"] = _db_path


@pytest.fixture(scope="session")
def _app():
    """Create a FastAPI app for testing (session-scoped)."""
    from main import app
    return app


@pytest.fixture
def app(_app):
    """Per-test app with fresh DB."""
    # Delete old temp DB and create fresh
    db_path = os.environ["DB_PATH"]
    if os.path.exists(db_path):
        os.unlink(db_path)
    
    from database import init_db
    init_db()
    
    # Clear caches and sessions
    import auth
    auth.SESSIONS.clear()
    auth._rate_limits.clear()
    import cache
    cache._cache.clear()
    
    return _app


@pytest.fixture
def client(app):
    """Test client using FastAPI TestClient."""
    from fastapi.testclient import TestClient
    return TestClient(app)


def pytest_sessionfinish():
    """Clean up temp DB at end of test session."""
    db_path = os.environ.get("DB_PATH", "")
    if db_path and os.path.exists(db_path):
        try:
            os.unlink(db_path)
        except OSError:
            pass
