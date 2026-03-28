import logging
from typing import List
from datetime import datetime, timezone

logger = logging.getLogger("trade_opportunities.data_collection")


class MarketNewsItem:
    """
    Simple value object representing a market news item.

    In a real implementation, this would likely be a Pydantic model
    or dataclass with more fields.
    """

    def __init__(self, title: str, source: str, url: str, published_at: datetime):
        self.title = title
        self.source = source
        self.url = url
        self.published_at = published_at

    def to_bullet_point(self) -> str:
        # Format as a markdown bullet point with date and source.
        date_str = self.published_at.astimezone(timezone.utc).strftime("%Y-%m-%d")
        return f"- [{self.title}]({self.url}) — {self.source}, {date_str} (UTC)"


async def fetch_sector_market_news(sector: str) -> List[MarketNewsItem]:
    """
    Temporary stub implementation for market data collection.

    Later this function will:
    - Call a web search API (e.g., DuckDuckGo or other)
    - Or perform lightweight scraping of news pages
    - Filter and normalize the results for the given sector

    """
    try:
        now = datetime.now(timezone.utc)

        # These are dummy items just to show structure.
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
    except Exception as exc:
        # When this becomes a real API call, this block will:
        # - Log the error with context
        # - Optionally re-raise a custom exception for the API layer
        logger.exception(
            "Failed to fetch market news for sector=%s due to unexpected error.",
            sector
        )
        # Returning an empty list here; the API layer decides how to handle this.
        return []

