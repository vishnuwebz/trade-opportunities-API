from dotenv import load_dotenv
import os
from typing import Optional

# Load .env file at import time
load_dotenv()

def get_env_str(name: str, default: Optional[str] = None) -> Optional[str]:
    """
    Helper to read environment variables.

    Returns:
        The value of the environment variable if set, otherwise the provided default.
    """
    return os.getenv(name, default)


# GNews-specific configuration
GNEWS_API_KEY_ENV = "GNEWS_API_KEY"
GNEWS_BASE_URL = "https://gnews.io/api/v4/search"