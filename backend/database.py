"""Database connection and schema management for Just4Tech."""

import sqlite3
import logging
from pathlib import Path

from config import DB_PATH

logger = logging.getLogger("just4tech.database")

# For in-memory databases, use shared cache so multiple connections
# see the same data (required for testing with connection-per-request).
_IS_MEMORY = DB_PATH == ":memory:"
_MEMORY_URI = "file::memory:?cache=shared"


def get_db() -> sqlite3.Connection:
    """Get a SQLite connection with WAL mode and foreign keys enabled."""
    if _IS_MEMORY:
        conn = sqlite3.connect(_MEMORY_URI, uri=True)
    else:
        Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(DB_PATH))

    conn.row_factory = sqlite3.Row
    if not _IS_MEMORY:
        conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """Initialize database schema. Idempotent — uses IF NOT EXISTS."""
    conn = get_db()
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT DEFAULT 'review',
            excerpt TEXT DEFAULT '',
            tags TEXT DEFAULT '',
            author TEXT DEFAULT 'AI Tool Hub Team',
            status TEXT DEFAULT 'published',
            cover_image TEXT DEFAULT '',
            icon TEXT DEFAULT '',
            subtitle TEXT DEFAULT '',
            external_url TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS site_pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slug TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            meta_title TEXT DEFAULT '',
            meta_description TEXT DEFAULT '',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS content_blocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_path TEXT NOT NULL,
            block_key TEXT NOT NULL,
            content TEXT NOT NULL DEFAULT '',
            content_type TEXT DEFAULT 'text',
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(page_path, block_key)
        );

        CREATE TABLE IF NOT EXISTS page_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            date TEXT NOT NULL,
            count INTEGER DEFAULT 1,
            UNIQUE(path, date)
        );

        CREATE TABLE IF NOT EXISTS page_visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL,
            ip_address TEXT DEFAULT '',
            country TEXT DEFAULT '',
            region TEXT DEFAULT '',
            city TEXT DEFAULT '',
            user_agent TEXT DEFAULT '',
            referer TEXT DEFAULT '',
            browser TEXT DEFAULT '',
            os TEXT DEFAULT '',
            device TEXT DEFAULT '',
            visited_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE INDEX IF NOT EXISTS idx_visits_path ON page_visits(path);
        CREATE INDEX IF NOT EXISTS idx_visits_date ON page_visits(visited_at);
        CREATE INDEX IF NOT EXISTS idx_visits_country ON page_visits(country);

        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS ai_config (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    logger.info("Database initialized at %s", DB_PATH)
