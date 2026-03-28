
# Trade Opportunities API

A FastAPI-based service that analyzes market data and generates trade opportunity reports
for specific sectors in India using GNews and Google Gemini.

## Features

- Single endpoint: `GET /analyze/{sector}` (e.g. `/analyze/pharmaceuticals`)
- Fetches recent sector-specific news from GNews (with stub fallback)
- Uses Google Gemini to generate a structured markdown report:
  - Overview
  - Key Opportunities
  - Risks and Challenges
  - Suggested Next Steps
  - Conclusion
- API key-based authentication via `X-API-Key` header
- In-memory session tracking and per-session rate limiting
- Graceful error handling and centralized logging

## Tech Stack

- **Backend**: FastAPI (async)
- **HTTP client**: httpx (async)
- **LLM**: Google Gemini (via `google-genai` Python SDK)
- **News data**: GNews free-tier API
- **Storage**: In-memory (Python dictionaries)
- **Auth**: Simple API key header + in-memory sessions
- **Rate limiting**: Fixed window (10 req/min per API key)

## Project Structure

```text
.
├── core
│   ├── __init__.py
│   ├── auth.py              # API key auth, sessions, rate limiting
│   ├── config.py            # Env var helpers and GNews config
│   └── logging_config.py    # Application-wide logging
├── services
│   ├── __init__.py
│   ├── data_collection.py   # GNews integration + stub fallback
│   └── ai_analysis.py       # Gemini integration + markdown composer
├── main.py                  # FastAPI app and /analyze/{sector} endpoint
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone and create virtual environment

```bash
cd C:\Users\vishn\OneDrive\Desktop
git clone https://github.com/vishnuwebz/trade-opportunities-API
cd trade-opportunities-api

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

### 2. Configure environment variables

#### GNews (news data)

1. Sign up at https://gnews.io and get a free-tier API key (100 requests/day, 10 articles per request, 12h delay).[web:8]
2. Set the key as an environment variable:

PowerShell:

```powershell
$env:GNEWS_API_KEY = "YOUR_GNEWS_API_KEY_HERE"
```

CMD:

```cmd
set GNEWS_API_KEY=YOUR_GNEWS_API_KEY_HERE
```

The service will still work with stubbed data if this is not set.

#### Gemini (LLM)

1. Enable the Gemini API at https://ai.google.dev and create an API key for your project.[web:20]
2. Set it as an environment variable:

PowerShell:

```powershell
$env:GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"
```

CMD:

```cmd
set GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
```

If the key is missing or invalid, the service falls back to a deterministic markdown template.

### 3. Run the FastAPI application

```bash
venv\Scripts\activate
uvicorn main:app --reload
```

- API root: http://127.0.0.1:8000
- Interactive docs (Swagger UI): http://127.0.0.1:8000/docs
- ReDoc docs: http://127.0.0.1:8000/redoc

## Usage

### Authentication

Every request to `/analyze/{sector}` must include an `X-API-Key` header:

- Example header: `X-API-Key: test-client-123`
- Each distinct API key is treated as a separate session
- Rate limit: 10 requests per minute per API key (HTTP 429 when exceeded)

### Example request

```bash
curl -X GET "http://127.0.0.1:8000/analyze/pharmaceuticals" ^
  -H "X-API-Key: test-client-123"
```

Example response (JSON):

```json
{
  "sector": "pharmaceuticals",
  "report_markdown": "# Trade Opportunities Report: Pharmaceuticals\n\n..."
}
```

The `report_markdown` field contains a structured markdown report that can be saved as a `.md` file.

## Design Notes

- **Separation of concerns**
  - `main.py`: request validation, dependency injection, endpoint wiring
  - `services.data_collection`: external news API access (GNews), stub fallback, error handling
  - `services.ai_analysis`: Gemini integration and markdown report composition
  - `core.auth`: authentication, session tracking, and rate limiting
  - `core.logging_config`: centralized logging configuration

- **Error handling**
  - External API failures (GNews, Gemini) are caught, logged, and replaced with fallback behavior
  - The API still returns a valid markdown report even when external services fail

- **Security & rate limiting**
  - Simple API key auth via `X-API-Key` header
  - In-memory session store mapping API key → session info
  - Fixed-window rate limiter (10 req/min per session) using timestamps
  - HTTP 401 for missing API key, HTTP 429 when rate limit exceeded

## Possible Extensions

- Add more endpoints (e.g. `/sectors` listing, saved reports)
- Swap GNews for another news provider by updating `data_collection.py`
- Add unit tests for services and rate limiting
- Containerize with Docker for easier deployment

