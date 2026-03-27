from fastapi import FastAPI, HTTPException, Path, Depends
from pydantic import BaseModel

from services.data_collection import fetch_sector_market_news
from services.ai_analysis import generate_sector_report_markdown
from core.auth import SessionInfo, get_current_session  # NEW import

app = FastAPI(title="Trade Opportunities API", version="0.1.0")


class AnalysisResponse(BaseModel):
    sector: str
    report_markdown: str


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get(
    "/analyze/{sector}",
    response_model=AnalysisResponse,
    summary="Analyze trade opportunities for a sector",
    description="Returns a markdown report with trade opportunity insights for the given sector in India.",
)
async def analyze_sector(
    sector: str = Path(
        ...,
        min_length=3,
        max_length=50,
        description="Sector name to analyze, e.g., pharmaceuticals, technology, agriculture.",
    ),
    session: SessionInfo = Depends(get_current_session),  # NEW dependency
):
    """
    Implementation overview:

    1. Enforce API key-based authentication via get_current_session.
    2. Validate and normalize the sector input.
    3. Delegate market data collection to the data_collection service.
    4. Delegate markdown report generation to the AI analysis service.

    In the final version:
    - data_collection will fetch real market/news data using web search or APIs.
    - ai_analysis will call an LLM (e.g., Gemini) to analyze that data and produce a richer report.
    - session information will be used to apply per-session rate limiting.
    """
    # session is currently not used directly in logic, but:
    # - It ensures authentication.
    # - It increments request_count and updates last_seen_at, preparing for rate limiting.

    normalized_sector = sector.strip().lower()

    if not normalized_sector.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Sector must contain only alphabetic characters.",
        )

    news_items = await fetch_sector_market_news(normalized_sector)

    report_markdown = await generate_sector_report_markdown(
        normalized_sector, news_items
    )

    return AnalysisResponse(sector=normalized_sector, report_markdown=report_markdown)