from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, List

from fastapi import Depends, Header, HTTPException, status


class SessionInfo:
    """
    In-memory representation of a client session associated with an API key.
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.created_at = datetime.now(timezone.utc)
        self.last_seen_at = self.created_at
        self.request_count = 0  # This will be used for rate limiting.
        self.request_timestamps: List[datetime] = []  # for rate limiting


# Simple in-memory store: api_key -> SessionInfo
_session_store: Dict[str, SessionInfo] = {}


def get_or_create_session(api_key: str) -> SessionInfo:
    """
    Retrieve existing session for API key or create a new one.
    """
    session = _session_store.get(api_key)
    if session is None:
        session = SessionInfo(api_key=api_key)
        _session_store[api_key] = session

    session.last_seen_at = datetime.now(timezone.utc)
    session.request_count += 1
    return session




async def get_current_session(
    x_api_key: Optional[str] = Header(
        default=None,
        alias="X-API-Key",
        description="API key used for authenticating and tracking sessions.",
    )
) -> SessionInfo:
    """
    FastAPI dependency that:
    - Validates presence of an API key header.
    - Retrieves or creates a session associated with that key.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header.",
        )

    # In a more advanced setup, you might validate this key against a database
    # or configuration. Here, any non-empty key is treated as a valid client identifier.
    session = get_or_create_session(x_api_key)
    return session


RATE_LIMIT_REQUESTS = 10
RATE_LIMIT_WINDOW = timedelta(minutes=1)


def _enforce_rate_limit(session: SessionInfo) -> None:
    """
    Enforce a simple fixed-window rate limit per session.

    - Allow up to RATE_LIMIT_REQUESTS within RATE_LIMIT_WINDOW.
    - If exceeded, raise HTTP 429 Too Many Requests.
    """
    now = datetime.now(timezone.utc)
    window_start = now - RATE_LIMIT_WINDOW

    # Keep only timestamps within the current window.
    session.request_timestamps = [
        ts for ts in session.request_timestamps if ts >= window_start
    ]

    if len(session.request_timestamps) >= RATE_LIMIT_REQUESTS:
        # Client exceeded the rate limit.
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=(
                f"Rate limit exceeded: maximum {RATE_LIMIT_REQUESTS} requests "
                f"per {int(RATE_LIMIT_WINDOW.total_seconds() // 60)} minute(s) allowed."
            ),
        )

    # Record the current request.
    session.request_timestamps.append(now)


async def get_rate_limited_session(
    session: SessionInfo = Depends(get_current_session),
) -> SessionInfo:
    """
    FastAPI dependency that:
    - Ensures the client is authenticated (via get_current_session).
    - Applies rate limiting based on recent request timestamps.
    """
    _enforce_rate_limit(session)
    return session