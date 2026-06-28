"""Simple in-memory response cache with TTL."""

import logging
from datetime import datetime
from functools import wraps

logger = logging.getLogger("just4tech.cache")

_cache: dict[str, dict] = {}


def cached(key: str, ttl_seconds: int = 300):
    """Decorator: cache async function result for `ttl_seconds`. Keyed by `key`."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            entry = _cache.get(key)
            if entry and (datetime.now() - entry["ts"]).total_seconds() < ttl_seconds:
                logger.debug("Cache hit: %s", key)
                return entry["data"]
            logger.debug("Cache miss: %s", key)
            result = await func(*args, **kwargs)
            _cache[key] = {"ts": datetime.now(), "data": result}
            return result
        return wrapper
    return decorator


def invalidate_cache(*keys: str) -> None:
    """Invalidate specific cache entries (e.g., on content change)."""
    for k in keys:
        if k in _cache:
            del _cache[k]
            logger.debug("Cache invalidated: %s", k)
