# AI Chat Service with Real-Time Token Tracking

This project is a full-stack Python application that allows users to engage in conversations with an AI model while tracking session history and the exact cost of each message based on token usage.

## Features
- **FastAPI Backend:** High-performance API with automated Swagger documentation.
- **Session Management:** Unique UUID-based chat sessions with persistent memory.
- **Persistent Storage:** Uses SQLAlchemy and SQLite to store message history and costs.
- **Token Analytics:** Real-time calculation of input/output tokens and cost tracking for models like gpt-4o-mini.
- **Streamlit UI:** Clean and interactive frontend for a seamless user experience.

## Project Structure
- `main.py` - FastAPI routes and core application logic.
- `service.py` - OpenAI integration and token cost calculation.
- `schemas.py` - Pydantic models for data validation.
- `models.py` & `database.py` - SQLAlchemy models and database configuration.
- `ui.py` - Streamlit-based user interface.
- `.env` - (Local only) Environment variables for API keys (never pushed to GitHub).

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd aichat

2. **Set up Environment Variables:**
    ```bash
    OPENAI_API_KEY=sk-your-key-here
    DATABASE_URL=sqlite:///./sql_app.db

3. **Install Dependencies:**
    ```bash
    uv sync

4. **Run the Backend:**
    ```bash
    uv run uvicorn main:app --reload

5. **Run the Frontend:**
    ```bash
    uv run streamlit run ui.py