import logging
from datetime import datetime, timezone
from typing import List, Optional

import httpx

from core.config import get_env_str, GNEWS_API_KEY_ENV, GNEWS_BASE_URL

logger = logging.getLogger("trade_opportunities.data_collection")


class MarketNewsItem:
    def __init__(self, title: str, source: str, url: str, published_at: datetime):
        self.title = title
        self.source = source
        self.url = url
        self.published_at = published_at

    def to_bullet_point(self) -> str:
        date_str = self.published_at.astimezone(timezone.utc).strftime("%Y-%m-%d")
        return f"- [{self.title}]({self.url}) — {self.source}, {date_str} (UTC)"


async def _fetch_news_from_gnews(sector: str) -> List[MarketNewsItem]:
    """
    Fetch news items from the GNews API using httpx.

    GNews free plan characteristics:
    - 100 requests per day.
    - Up to 10 articles per request.
    - 12-hour delay for free tier content.
    This is suitable for development and this assignment demo.[web:8]
    """
    api_key = get_env_str(GNEWS_API_KEY_ENV)
    if not api_key:
        logger.warning(
            "GNEWS_API_KEY not configured; falling back to stub data for sector=%s",
            sector,
        )
        return _build_stub_news(sector)

    params = {
        "q": f"{sector} sector India",
        "lang": "en",
        "country": "in",
        "max": 10,  # up to 10 articles on free plan.[web:8]
        "token": api_key,
    }

    logger.info("Calling GNews API for sector=%s", sector)

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(GNEWS_BASE_URL, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            logger.error(
                "GNews API returned HTTP %s for sector=%s: %s",
                exc.response.status_code,
                sector,
                exc.response.text[:200],
            )
            return []
        except httpx.RequestError as exc:
            logger.error(
                "Failed to reach GNews API for sector=%s: %s", sector, str(exc)
            )
            return []

    data = response.json()
    articles = data.get("articles", [])
    items: List[MarketNewsItem] = []

    for article in articles:
        title = article.get("title") or "Untitled article"
        source_name = (article.get("source") or {}).get("name") or "Unknown source"
        url = article.get("url") or "#"
        published_at_str: Optional[str] = article.get("publishedAt")

        try:
            if published_at_str:
                # GNews returns ISO-8601 like "2024-03-01T10:00:00Z"
                published_dt = datetime.fromisoformat(
                    published_at_str.replace("Z", "+00:00")
                )
            else:
                published_dt = datetime.now(timezone.utc)
        except Exception:
            published_dt = datetime.now(timezone.utc)

        items.append(
            MarketNewsItem(
                title=title,
                source=source_name,
                url=url,
                published_at=published_dt,
            )
        )

    logger.info("Fetched %d news items from GNews for sector=%s", len(items), sector)
    return items


def _build_stub_news(sector: str) -> List[MarketNewsItem]:
    now = datetime.now(timezone.utc)

    logger.info("Using stubbed news items for sector=%s", sector)

    return [
        MarketNewsItem(
            title=f"Recent investment trends in the {sector} sector in India",
            source="Example News",
            url="https://example.com/article1",
            published_at=now,
        ),
        MarketNewsItem(
            title=f"Government policy updates impacting the {sector} industry",
            source="Policy Insights",
            url="https://example.com/article2",
            published_at=now,
        ),
        MarketNewsItem(
            title=f"Export opportunities for Indian {sector} companies",
            source="Trade Watch",
            url="https://example.com/article3",
            published_at=now,
        ),
    ]


async def fetch_sector_market_news(sector: str) -> List[MarketNewsItem]:
    """
    Public entry point for market data collection.

    Attempts to use GNews via httpx.
    Falls back to stub data if configuration is missing or a failure occurs.
    """
    try:
        items = await _fetch_news_from_gnews(sector)
        if not items:
            # If external API returns nothing or errors occurred, fall back to stub.
            return _build_stub_news(sector)
        return items
    except Exception:
        logger.exception(
            "Unexpected error while fetching market news for sector=%s", sector
        )
        return _build_stub_news(sector)