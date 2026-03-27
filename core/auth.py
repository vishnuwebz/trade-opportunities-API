from datetime import datetime, timezone
from typing import Dict, Optional

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