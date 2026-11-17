# CreatorFlow

**CreatorFlow** is a Python-based media processing project designed to simplify file conversion and content preparation workflows for creators.

> 🚧 **Project status:** Early development. The API skeleton and health endpoint are available; media conversion is not implemented yet.

## Overview

CreatorFlow aims to provide a unified platform for processing images, videos, audio, and documents.

The long-term goal is to help content creators automate repetitive media preparation tasks.

## Current Functionality

- FastAPI application factory with configurable application metadata and debug mode.
- Environment-based configuration using Pydantic Settings.
- Health-check endpoint and automatically generated API documentation.
- Automated tests, code quality checks, and static type checking.

## Planned Features

- [ ] Image format conversion
- [ ] Video format conversion
- [ ] Audio processing
- [ ] Document conversion
- [ ] Batch file processing
- [ ] REST API for media processing

These features are planned and are not yet available as a complete application.

## Tech Stack

- **Python 3.12+** — Programming language
- **FastAPI** — Web API framework
- **Uvicorn** — ASGI server
- **Pydantic Settings** — Application configuration
- **uv** — Dependency and environment management
- **pytest and pytest-cov** — Automated testing and coverage
- **HTTPX** — HTTP client used by API tests
- **Ruff** — Linting and formatting
- **mypy** — Static type checking

## Getting Started

### Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/SAMSONOVprodby/creatorflow.git
cd creatorflow
```

Install dependencies from the committed lockfile:

```bash
uv sync --locked
```

### Configuration

The application uses Pydantic Settings. Default values are defined in `src/creatorflow/core/config.py`.

To customize local settings, copy `.env.example` to `.env`:

**PowerShell (Windows):**

```powershell
Copy-Item .env.example .env
```

**macOS/Linux:**

```bash
cp .env.example .env
```

Supported settings:

| Variable | Default | Description |
| --- | --- | --- |
| `APP_NAME` | `CreatorFlow` | Application title shown in API documentation |
| `APP_VERSION` | `0.1.0` | Application version |
| `DEBUG` | `false` | Enable or disable FastAPI debug mode |
| `ENVIRONMENT` | `development` | `development`, `testing`, or `production` |

The `.env` file is intended for local configuration and should not be committed. Use `.env.example` as the shareable template.

### Running the API

Start the development server from the repository root:

```bash
uv run uvicorn creatorflow.main:create_app --factory --reload
```

The server is available at `http://127.0.0.1:8000` by default. The `--factory` option tells Uvicorn to call `create_app()` to build the FastAPI application. `--reload` is intended for local development.

### API Endpoints

| Method | Path | Description | Expected response |
| --- | --- | --- | --- |
| `GET` | `/health` | Basic application health check | `200` with `{"status": "ok"}` |
| `GET` | `/docs` | Interactive Swagger UI | `200` |
| `GET` | `/openapi.json` | Generated OpenAPI schema | `200` |

The root path `/` is not implemented and currently returns `404 Not Found`.

## Development Checks

Run the test suite:

```bash
uv run pytest -v
```

Run tests with coverage and enforce the minimum 80% threshold:

```bash
uv run pytest --cov=creatorflow --cov-report=term-missing --cov-fail-under=80
```

Check linting, formatting, and types across application and test code:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
```

Check the dependency lockfile:

```bash
uv lock --check
```

Automatically format code:

```bash
uv run ruff format .
```

## Project Structure

```text
creatorflow/
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── creatorflow/
│       ├── api/
│       │   ├── routes/
│       │   │   └── health.py
│       │   └── router.py
│       ├── core/
│       │   └── config.py
│       ├── utils/
│       │   └── filenames.py
│       ├── __init__.py
│       ├── main.py
│       └── py.typed
├── tests/
│   ├── api/
│   │   └── test_health.py
│   ├── conftest.py
│   ├── test_config.py
│   ├── test_filenames.py
│   └── test_main.py
├── .env.example
├── pyproject.toml
├── uv.lock
└── README.md
```

The structure will evolve as new modules are introduced.

## Roadmap

1. [x] Establish project tooling and testing.
2. [x] Implement initial reusable filename utility.
3. [x] Introduce the FastAPI application skeleton, configuration, and health endpoint.
4. [ ] Implement the first media conversion functionality.
5. [ ] Add batch processing and expand media-processing API endpoints.

## License

No license has been specified yet.
