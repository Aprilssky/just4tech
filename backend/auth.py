"""Authentication: API key, session management, password hashing."""

import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from functools import wraps

from fastapi import Request, HTTPException

from config import API_KEY, SESSION_TTL_SECONDS, LOGIN_RATE_MAX, LOGIN_RATE_WINDOW

logger = logging.getLogger("just4tech.auth")

# ── API Key Auth ────────────────────────────────────────────────

def require_api_key(request: Request) -> bool:
    """Check X-API-Key header for machine-to-machine access."""
    return request.headers.get("X-API-Key", "") == API_KEY


def api_key_required(func):
    """Decorator: require API key OR valid admin session."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = kwargs.get("request")
        if request:
            if require_api_key(request):
                return await func(*args, **kwargs)
            user = check_session(request)
            if user:
                return await func(*args, **kwargs)
        raise HTTPException(
            status_code=401,
            detail="API key required. Set X-API-Key header or log in as admin.",
        )
    return wrapper


# ── Session Management ──────────────────────────────────────────

SESSIONS: dict[str, dict] = {}  # token → {username, expires_at}


def check_session(request: Request) -> str | None:
    """Validate session cookie, return username or None."""
    token = request.cookies.get("session")
    if not token:
        return None
    entry = SESSIONS.get(token)
    if not entry:
        return None
    if datetime.now() > entry["expires_at"]:
        del SESSIONS[token]
        return None
    return entry["username"]


def create_session(username: str) -> tuple[str, datetime]:
    """Create a new session, return (token, expires_at)."""
    _cleanup_expired_sessions()
    token = uuid.uuid4().hex
    expires = datetime.now() + timedelta(seconds=SESSION_TTL_SECONDS)
    SESSIONS[token] = {"username": username, "expires_at": expires}
    return token, expires


def destroy_session(token: str) -> None:
    """Remove a session by token."""
    SESSIONS.pop(token, None)


def update_session_username(token: str, new_username: str) -> None:
    """Update the username associated with a session token."""
    if token in SESSIONS:
        SESSIONS[token]["username"] = new_username


def _cleanup_expired_sessions() -> None:
    """Remove all expired sessions."""
    now = datetime.now()
    expired = [t for t, e in SESSIONS.items() if now > e["expires_at"]]
    for t in expired:
        del SESSIONS[t]


# ── Password Hashing ────────────────────────────────────────────

_bcrypt_module = None
_bcrypt_available: bool | None = None


def hash_password(password: str) -> str:
    """Hash password with bcrypt. Falls back to salted SHA-256 if bcrypt unavailable."""
    global _bcrypt_module, _bcrypt_available
    if _bcrypt_available is None:
        try:
            import bcrypt as _bcrypt
            _bcrypt_module = _bcrypt
            _bcrypt_available = True
        except ImportError:
            _bcrypt_available = False

    if _bcrypt_available:
        return _bcrypt_module.hashpw(password.encode(), _bcrypt_module.gensalt()).decode()
    else:
        import os as _os
        salt = _os.urandom(32).hex()
        return f"sha256${salt}${hashlib.sha256((salt + password).encode()).hexdigest()}"


def verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash. Supports bcrypt, salted SHA-256, and unsalted SHA-256."""
    if stored_hash.startswith(("$2b$", "$2a$")):
        import bcrypt as _bcrypt
        return _bcrypt.checkpw(password.encode(), stored_hash.encode())
    elif stored_hash.startswith("sha256$"):
        _, salt, h = stored_hash.split("$")
        return hashlib.sha256((salt + password).encode()).hexdigest() == h
    else:
        # Legacy: unsalted SHA-256
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash


# ── Rate Limiting ───────────────────────────────────────────────

_rate_limits: dict[str, tuple[int, datetime]] = {}


def check_rate_limit(key: str, max_requests: int = LOGIN_RATE_MAX,
                     window_seconds: int = LOGIN_RATE_WINDOW) -> bool:
    """Return True if request is allowed, False if rate-limited."""
    now = datetime.now()
    entry = _rate_limits.get(key)
    if entry:
        count, start = entry
        if (now - start).total_seconds() < window_seconds:
            if count >= max_requests:
                logger.warning("Rate limit hit for key=%s", key[:20])
                return False
            _rate_limits[key] = (count + 1, start)
        else:
            _rate_limits[key] = (1, now)
    else:
        _rate_limits[key] = (1, now)
    return True
