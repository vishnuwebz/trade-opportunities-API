from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

from services.data_collection import fetch_sector_market_news  # NEW import

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
    Temporary implementation that demonstrates:
    - Input validation on the sector path parameter
    - Delegation to a data collection layer
    - Basic markdown report composition

    Later this function will:
    - Collect recent market data/news for the sector using real web search
    - Call an LLM (e.g., Gemini) with that data
    - Generate a richer, AI-driven markdown report
    """
    normalized_sector = sector.strip().lower()

    if not normalized_sector.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Sector must contain only alphabetic characters.",
        )

    # Use the data collection layer (currently stubbed)
    news_items = await fetch_sector_market_news(normalized_sector)

    news_section_lines = [
        "## Recent Market News",
        "",
    ]
    if news_items:
        news_section_lines.extend(item.to_bullet_point() for item in news_items)
    else:
        news_section_lines.append(
            "- No recent news items found in the stub implementation."
        )

    news_section = "\n".join(news_section_lines)

    dummy_markdown = f"""# Trade Opportunities Report: {normalized_sector.title()}

## Overview

This is a placeholder report for the **{normalized_sector}** sector in India.
In the final implementation, this section will summarize the current market landscape and key growth drivers.

## Key Opportunities

- Opportunity 1: Example opportunity in the {normalized_sector} sector.
- Opportunity 2: Example opportunity in the {normalized_sector} sector.
- Opportunity 3: Example opportunity in the {normalized_sector} sector.

{news_section}

## Risks and Challenges

- Risk 1: Example regulatory or market risk.
- Risk 2: Example operational or supply chain challenge.

## Conclusion

This is a dummy conclusion. The final report will be generated using live market data and LLM analysis.
"""

    return AnalysisResponse(sector=normalized_sector, report_markdown=dummy_markdown)