"""Rate limiter for TwelveLabs API."""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Track and enforce TwelveLabs API rate limits."""

    LIMITS = {
        'search': 50,
        'analyze': 50,  # Analyze endpoint
        'summarize': 50,
        'generate': 50,
        'embed': 100,
        'task': 50,
    }

    def __init__(self, state_file: str = "/tmp/twelvelabs_rate_limit.json"):
        self.state_file = Path(state_file)
        self.state = self._load_state()

    def _load_state(self) -> dict:
        """Load rate limit state from file."""
        if not self.state_file.exists():
            return self._reset_state()

        try:
            with open(self.state_file, 'r') as f:
                state = json.load(f)

            # Check if we need to reset (new day)
            last_reset = datetime.fromisoformat(state['last_reset'])
            if datetime.utcnow().date() > last_reset.date():
                return self._reset_state()

            return state
        except Exception:
            return self._reset_state()

    def _reset_state(self) -> dict:
        """Reset daily counters."""
        state = {
            'last_reset': datetime.utcnow().isoformat(),
            'usage': {endpoint: 0 for endpoint in self.LIMITS.keys()}
        }
        self._save_state(state)
        return state

    def _save_state(self, state: dict) -> None:
        """Save state to file."""
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def can_make_request(self, endpoint: str) -> bool:
        """Check if we can make a request to this endpoint."""
        if endpoint not in self.LIMITS:
            return True

        current = self.state['usage'].get(endpoint, 0)
        limit = self.LIMITS[endpoint]
        return current < limit

    def get_remaining(self, endpoint: str) -> int:
        """Get remaining calls for endpoint today."""
        if endpoint not in self.LIMITS:
            return 999

        current = self.state['usage'].get(endpoint, 0)
        limit = self.LIMITS[endpoint]
        return max(0, limit - current)

    def record_request(self, endpoint: str) -> None:
        """Record that a request was made."""
        if endpoint not in self.state['usage']:
            self.state['usage'][endpoint] = 0

        self.state['usage'][endpoint] += 1
        self._save_state(self.state)

        remaining = self.get_remaining(endpoint)
        logger.info(f"📊 {endpoint}: {remaining}/{self.LIMITS[endpoint]} remaining today")

    def get_usage_summary(self) -> dict:
        """Get current usage across all endpoints."""
        summary = {}
        for endpoint, limit in self.LIMITS.items():
            used = self.state['usage'].get(endpoint, 0)
            summary[endpoint] = {
                'used': used,
                'limit': limit,
                'remaining': limit - used,
                'percentage': (used / limit) * 100 if limit > 0 else 0
            }
        return summary


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""
    pass
