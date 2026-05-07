# Pre-Campaign Intelligence

FastAPI backend that reviews a campaign *before launch* and returns an improved version of the same campaign payload (currently, only the `video_script` is rewritten). It combines:
- Rule-based analysis (sentiment, hook score, CTA score, pacing)
- Google Gemini critique + rewrite

## Tech Stack
- FastAPI
- Pydantic v2
- Google Gemini via `google-genai`
- VADER sentiment (`vadersentiment`)
- `uvicorn` for serving
- `dotenv` loader (reads [.env](.env))

## Project Layout (Ports & Adapters / Hexagonal-ish)
- Domain models: [src/domain/models/](src/domain/models/)
- Ports (interfaces): [src/ports/](src/ports/)
- Adapters (implementations): [src/adapters/](src/adapters/)
- Application services (use-cases + DI wiring): [src/application/services/](src/application/services/)
- Config: [src/config/](src/config/)
- Dummy data: [dummy_data/](dummy_data/)

## Requirements
- Python (as configured in [pyproject.toml](pyproject.toml): `requires-python = ">=3.14"`)
- Google API key:
  - `GOOGLE_GENERATIVE_AI_API_KEY`

## Setup

### Using uv (recommended)
```bash
uv sync