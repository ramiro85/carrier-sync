# AGENTS.md — Python / API Project

This file provides guidance for AI agents (Codex, Claude, Cursor, Copilot, etc.) working in this codebase. Read it fully before making any changes.

---

## Project Overview
An API to use third part service like TAFS, Safer, ELD
## Environment Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies (including dev tools)
pip install -r requirements.txt

# 3. Copy env template and fill in values
cp .env.example .env
# 6. Start the development server
uvicorn app.main:app --reload
```
The API will be available at `http://localhost:8000`.  
Interactive docs: `http://localhost:8000/docs` (Swagger) and `/redoc`.

## Configuration
Configuration is managed through `api/config.py` and environment variables in `.env`.

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    attachment_path: str 
    gcp_project_id: str 
    gcp_region: str 

    class Config:
        env_file = ".env"

settings = Settings()
```

**Never hardcode credentials.** Always use environment variables for:
- Database connection strings
- API keys for external services (TAFS, Safer, Reliable)
- Authentication secrets
- Third-party service URLs

---

## Coding Conventions

### General

- Use **Python 3.10+ type hints** where possible — functions, return values, class attributes.
- Follow the **module-based architecture**: `tafs/`, `safer/`, `eld/` for domain-specific code.
- Keep route handlers in `endpoints.py` files.
- Business logic and external API integration belongs in `controller.py` files.
- Use the structured logger from `app/utils/logging.py` — **never `print()`**.
- Shared utilities belong in `core/utils.py`.

## Linting & Formatting

```bash
# Format code
black app tests

# Lint (auto-fix safe issues)
ruff check app tests --fix

# Type check
mypy app
```
All three must pass with zero errors before a PR is merged. CI enforces this.

## Adding a New Feature (Checklist)

When adding a new resource or endpoint, follow this order:

- [ ] Define/update the **ORM model** in `api/models/`
- [ ] Add **routes** in `api/routers/` and register the router in `main.py`
- [ ] Add or update **dependencies** in `app/dependencies.py` if needed
- [ ] Write **tests** in `tests/routers/`
- [ ] Update **OpenAPI tags/descriptions** if the endpoint is public-facing
- [ ] Update this `AGENTS.md` if you introduce new patterns or conventions

## What Agents Should NOT Do

- **Do not** modify `.env` or commit secrets to the repository.
- **Do not** disable Mypy, Ruff, or Black checks — fix the underlying issue instead.

## Contact & Ownership

| Area                  | Owner     |
|-----------------------|-----------|
| API design            | TBD |
| Auth / security       | TBD |
| CI / DevOps           | TBD |
