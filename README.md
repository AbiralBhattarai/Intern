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
```

## Folder Structure

```text
pre-campaign-intelligence/
  .env
  .python-version
  main.py
  pyproject.toml
  README.md
  dummy_data/
    .gitignore
    campaign_dummy_data.json
  src/
    adapters/
      AiServiceAdapter.py
      CampaignAnalyzerAdapter.py
    application/
      services/
        CampaignAnalysisService.py
        CampaignReiterateService.py
        OrchestrationService.py
    config/
      ai_model_config.py
      cta_words_config.py
      hook_words_config.py
    domain/
      contract/
        SentimentAnalyzer.py
      models/
        CampaignDataInputModel.py
        CampaignDataOutputModel.py
        enums.py
    ports/
      input/
        CampaignAnalyzerPort.py
      output/
        AiServicePort.py
    utils/
      get_dummy_campaign_data.py
