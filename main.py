from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

from services.data_collection import fetch_sector_market_news
from services.ai_analysis import generate_sector_report_markdown  # NEW import

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
    )
):
    """
    Implementation overview:

    1. Validate and normalize the sector input.
    2. Delegate market data collection to the data_collection service.
    3. Delegate markdown report generation to the AI analysis service.

    In the final version:
    - data_collection will fetch real market/news data using web search or APIs.
    - ai_analysis will call an LLM (e.g., Gemini) to analyze that data and produce a richer report.
    """
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