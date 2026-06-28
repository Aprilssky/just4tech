"""Application configuration — all settings in one place, no hardcoded paths."""

import os as _os
import secrets as _secrets
from pathlib import Path as _Path

# ── Base paths ──────────────────────────────────────────────────
BASE_DIR = _Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"
UPLOAD_DIR = STATIC_DIR / "uploads"
ICON_CACHE_DIR = STATIC_DIR / "icon-cache"

# ── Deployment paths (overridable via env) ──────────────────────
# These are server-side paths used by the deployment scripts.
# Defaults match the existing production layout on tc server.
NGINX_SPA_DIR = _os.environ.get("NGINX_SPA_DIR", "/var/www/aitoolhub/spa")
NGINX_UPLOAD_DIR = _os.environ.get("NGINX_UPLOAD_DIR", f"{NGINX_SPA_DIR}/uploads")
API_KEY_FILE = _os.environ.get("API_KEY_FILE", "/etc/aitoolhub/api_key")
API_KEY_ENV_FILE = _os.environ.get("API_KEY_ENV_FILE", "/etc/aitoolhub/api_key_env")

# ── Server ──────────────────────────────────────────────────────
SERVER_HOST = _os.environ.get("HOST", "127.0.0.1")
SERVER_PORT = int(_os.environ.get("PORT", "8083"))
DEV_MODE = _os.environ.get("DEV_MODE", "").lower() in ("1", "true", "yes")

# ── Security ────────────────────────────────────────────────────
SESSION_TTL_SECONDS = 86400 * 7  # 7 days
LOGIN_RATE_MAX = 5
LOGIN_RATE_WINDOW = 60  # seconds
UPLOAD_MAX_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_UPLOAD_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}

# ── CORS ────────────────────────────────────────────────────────
CORS_ORIGINS = [
    "https://just4.tech",
    "https://www.just4.tech",
]
CORS_ORIGIN_REGEX = r"^https?://localhost(:\d+)?$"

# ── Icon proxy ──────────────────────────────────────────────────
ICON_MAX_SIZE = 512 * 1024  # 512 KiB
ICON_FETCH_TIMEOUT = 5.0    # seconds
ICON_CACHE_MAX_AGE = 604800  # 7 days in seconds
ICON_FETCH_HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Just4Tech/1.0; +https://just4.tech)",
    "Accept": "image/avif,image/webp,image/png,image/svg+xml,image/*;q=0.8,*/*;q=0.5",
}

# ── Cache TTLs ──────────────────────────────────────────────────
RSS_CACHE_TTL = 600   # 10 minutes
SITEMAP_CACHE_TTL = 900  # 15 minutes

# ── Contact email ───────────────────────────────────────────────
EMAIL_WEBHOOK_URL = _os.environ.get("EMAIL_WEBHOOK_URL", "http://localhost:18085/send-email")

# ── Database ────────────────────────────────────────────────────
DB_PATH = _os.environ.get("DB_PATH", str(DATA_DIR / "aitoolhub.db"))

# ── API Key ─────────────────────────────────────────────────────
def load_api_key() -> str:
    """Load API key: priority: key file → API_KEY env → MCP_API_KEY env."""
    # 1. Key file (most authoritative, written by CI/CD)
    if _os.path.isfile(API_KEY_FILE):
        try:
            key = _Path(API_KEY_FILE).read_text().strip()
            if key:
                return key
        except Exception:
            pass
    # 2. Environment variables (fallback for local dev)
    key = _os.environ.get("API_KEY") or _os.environ.get("MCP_API_KEY")
    if key:
        return key
    raise RuntimeError(
        "API_KEY is required. Set via key file or environment variable. "
        "Generate one with: python3 -c 'import secrets; print(secrets.token_hex(24))'"
    )

API_KEY = load_api_key()
