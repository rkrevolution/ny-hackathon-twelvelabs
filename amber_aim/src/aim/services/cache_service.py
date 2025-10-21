"""Caching service for TwelveLabs API responses."""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any, Optional

import logging

logger = logging.getLogger(__name__)


class CacheService:
    """Cache TwelveLabs API responses to avoid redundant calls."""

    def __init__(self, cache_dir: str = "/tmp/twelvelabs_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(days=7)  # Cache for 7 days

    def _get_cache_key(self, endpoint: str, params: dict) -> str:
        """Generate unique cache key."""
        params_str = json.dumps(params, sort_keys=True)
        key_str = f"{endpoint}:{params_str}"
        return hashlib.md5(key_str.encode()).hexdigest()

    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache key."""
        return self.cache_dir / f"{cache_key}.json"

    def get(self, endpoint: str, params: dict) -> Optional[dict]:
        """Get cached result if available and not expired."""
        cache_key = self._get_cache_key(endpoint, params)
        cache_path = self._get_cache_path(cache_key)

        if not cache_path.exists():
            return None

        try:
            with open(cache_path, 'r') as f:
                cached = json.load(f)

            # Check expiration
            cached_at = datetime.fromisoformat(cached['cached_at'])
            if datetime.utcnow() - cached_at > self.ttl:
                cache_path.unlink()
                return None

            logger.info(f"✅ Cache HIT for {endpoint}")
            return cached['data']

        except Exception as e:
            logger.warning(f"Cache error: {e}")
            if cache_path.exists():
                cache_path.unlink()
            return None

    def set(self, endpoint: str, params: dict, data: Any) -> None:
        """Cache API response."""
        cache_key = self._get_cache_key(endpoint, params)
        cache_path = self._get_cache_path(cache_key)

        cached = {
            'endpoint': endpoint,
            'params': params,
            'data': data,
            'cached_at': datetime.utcnow().isoformat()
        }

        with open(cache_path, 'w') as f:
            json.dump(cached, f, indent=2)

        logger.info(f"💾 Cached {endpoint} result")
