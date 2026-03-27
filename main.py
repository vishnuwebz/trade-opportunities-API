from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel

app = FastAPI(title="Trade Opportunities API", version="0.1.0")


class AnalysisResponse(BaseModel):
    sector: str
    report_markdown: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/analyze/{sector}",
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
    Temporary dummy implementation.

    Later this function will:
    - Collect recent market data/news for the sector
    - Call an LLM (e.g., Gemini) with that data
    - Generate a structured markdown report
    """

    normalized_sector = sector.strip().lower()

    if not normalized_sector.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Sector must contain only alphabetic characters.",
        )

    dummy_markdown = f""" # Trade Opportunities Report: {normalized_sector.title()}
    
    ## Overview
    
    This is a placeholder report for the **{normalized_sector}** sector in India.
    In the final implementation, this section will summarize the current market landscape and key growth drivers.
    
    ## Key Opportunities
    
    - Opportunity 1: Example opportunity in the  {normalized_sector} sector.
    - Opportunity 2: Example opportunity in the  {normalized_sector} sector.
    - Opportunity 3: Example opportunity in the  {normalized_sector} sector.
    
    ## Risks and Challenges
    
    - Risk 1: Example regularly or market risk.
    - Risk 2: Example operational or support chain challenge.
    
    ## Conclusion
    
    This is a dummy conclusion. The final report will be generated using live market data and LLM analysis.
"""

    return AnalysisResponse(sector=normalized_sector, report_markdown=dummy_markdown)