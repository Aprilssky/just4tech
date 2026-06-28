"""FastAPI dependencies for common patterns."""

from fastapi import Request, HTTPException

from auth import check_session, require_api_key


def get_current_user(request: Request) -> str:
    """Dependency: require authenticated session, return username."""
    user = check_session(request)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


def get_auth(request: Request) -> str | None:
    """Dependency: try session auth, return username or None (no error)."""
    return check_session(request)


def require_auth(request: Request) -> str:
    """Dependency: require API key OR session, return username or 'api_key'."""
    if require_api_key(request):
        return "api_key"
    user = check_session(request)
    if user:
        return user
    raise HTTPException(
        status_code=401,
        detail="API key required. Set X-API-Key header or log in as admin.",
    )
