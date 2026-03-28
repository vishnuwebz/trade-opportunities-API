# Trade Opportunities API

A FastAPI-based service that analyzes market data and generates trade opportunity reports
for specific sectors in India using GNews and Google Gemini.

---

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
- Optional React frontend to visualize markdown reports

---

## Tech Stack

- **Backend**: FastAPI (async)
- **HTTP client**: httpx (async)
- **LLM**: Google Gemini (via `google-genai` Python SDK)
- **News data**: GNews free-tier API
- **Storage**: In-memory (Python dictionaries)
- **Auth**: Simple API key header + in-memory sessions
- **Rate limiting**: Fixed window (10 req/min per API key)
- **Frontend (optional)**: React + Vite + `react-markdown`

---

## Project Structure

```text
trade-opportunities-api/
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
├── trade-opportunities-frontend/   # Optional React frontend (Vite)
│   ├── index.html
│   ├── package.json
│   └── src/
└── README.md
```

---

## Backend Setup Instructions

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

You can either set them manually in the shell, or create a `.env` file (not committed) based on `.env.example`.

#### GNews (news data)

1. Sign up at https://gnews.io and get a free-tier API key (100 requests/day, up to 10 articles per request, 12h delay).
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

1. Enable the Gemini API at https://ai.google.dev and create an API key for your project.
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

> For local development, you can create a `.env` file in the backend folder:
>
> ```env
> GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
> GNEWS_API_KEY=YOUR_GNEWS_API_KEY_HERE
> ```
>
> and `core.config` will load it automatically.

### 3. CORS configuration for frontend (development)

If you use the optional React frontend on `localhost:5173`, add CORS middleware in `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Trade Opportunities API", version="0.1.0")

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows the frontend to call the backend from the browser during development.

### 4. Run the FastAPI application

```bash
cd C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api
venv\Scripts\activate
uvicorn main:app --reload
```

- API root: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## Usage (Backend API)

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

---

## Optional Frontend (React)

A small React app is included under the backend folder:

```text
C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api\trade-opportunities-frontend
```

### Frontend Tech Stack

- React (Vite)
- `react-markdown` for rendering the markdown report
- Fetch-based calls to the FastAPI backend

### Frontend Setup

From the backend root folder:

```bash
cd C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api
cd trade-opportunities-frontend
npm install
npm install react-markdown
```

(If you haven't created it yet, you can initialize it with Vite from inside `trade-opportunities-api`:

```bash
cd C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api
npm create vite@latest trade-opportunities-frontend -- --template react
cd trade-opportunities-frontend
npm install
npm install react-markdown
```)

Replace `src/App.jsx` with a component that:

- Accepts `sector` and `X-API-Key` as inputs.
- Calls:

  ```text
  GET http://127.0.0.1:8000/analyze/{sector}
  Header: X-API-Key: <your-api-key>
  ```

- Renders `report_markdown` using `react-markdown`.

Example (simplified) fetch in React:

```js
const res = await fetch(
  `http://127.0.0.1:8000/analyze/${encodeURIComponent(sector)}`,
  {
    headers: {
      "X-API-Key": apiKey,
    },
  }
);
const data = await res.json();
setReportMarkdown(data.report_markdown);
```

### Running frontend + backend together

1. Start the backend:

```bash
cd C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api
venv\Scripts\activate
uvicorn main:app --reload
```

2. Start the frontend (from inside the nested folder):

```bash
cd C:\Users\vishn\OneDrive\Desktop\trade-opportunities-api\trade-opportunities-frontend
npm run dev
```

3. Open `http://localhost:5173` in a browser:
   - Enter a sector (e.g. `technology`) and API key (e.g. `test-client-123`).
   - Click **Generate Report** to see the Gemini-generated markdown nicely rendered.

---

## Design Notes

- **Separation of concerns**
  - `main.py`: request validation, dependency injection, endpoint wiring
  - `services.data_collection`: external news API access (GNews), stub fallback, error handling
  - `services.ai_analysis`: Gemini integration and markdown report composition
  - `core.auth`: authentication, session tracking, and rate limiting
  - `core.logging_config`: centralized logging configuration
  - `trade-opportunities-frontend`: independent React app consuming the API

- **Error handling**
  - External API failures (GNews, Gemini) are caught, logged, and replaced with fallback behavior
  - The API still returns a valid markdown report even when external services fail

- **Security & rate limiting**
  - Simple API key auth via `X-API-Key` header
  - In-memory session store mapping API key → session info
  - Fixed-window rate limiter (10 req/min per session) using timestamps
  - HTTP 401 for missing API key, HTTP 429 when rate limit exceeded

---

```