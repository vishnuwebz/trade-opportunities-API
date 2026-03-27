# 📈 Trade Opportunities API

A **FastAPI-based API** that analyzes trade opportunities by combining **recent market data** with insights from an **LLM (Google Gemini)**.  
The API returns a **well-structured Markdown report** highlighting sector-specific opportunities (e.g., pharmaceuticals), while demonstrating **clean architecture, security, and rate limiting**.

---

## 🚀 Features

- **FastAPI**: Lightweight, high-performance web framework
- **LLM Integration**: Calls Google Gemini via `google-generativeai` SDK
- **Market Data Fetching**:
  - Web scraping with `httpx` + `BeautifulSoup`
  - External APIs for sector-specific data
- **Markdown Reports**: Structured trade opportunity analysis
- **Security**: Simple token-based authentication
- **Rate Limiting**: Prevents abuse with in-memory counters
- **Validation**: Pydantic models for request/response schemas
- **Docs**: Auto-generated Swagger UI at `/docs`

---

## 🛠️ Tech Stack

- **FastAPI** – API framework  
- **Uvicorn** – ASGI server (`uvicorn main:app --reload`)  
- **httpx / requests** – HTTP client for APIs & scraping  
- **BeautifulSoup** – HTML parsing for scraped data  
- **google-generativeai** – Gemini LLM integration  
- **Pydantic** – Input validation & response models  
- **In-memory storage** – Rate limiting & caching  

---



