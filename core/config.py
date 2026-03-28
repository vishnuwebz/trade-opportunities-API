import os
from typing import Optional


def get_env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Helper to read environment variables.

    Returns:
        The value of the environment variable if set, otherwise the provided default.
    """
    return os.getenv(name, default)


# GNews-specific configuration
GNEWS_API_KEY_ENV = "e9baa635867a89f1a72b5285a8c722b1"
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"