# CreatorFlow

**CreatorFlow** is a Python-based media processing project designed to simplify file conversion and content preparation workflows for creators.

> 🚧 **Project status:** Early development. The image conversion core (DEV-004) is implemented and tested. Image conversion is currently available as a Python service; an HTTP conversion endpoint is planned for DEV-005.

## Overview

CreatorFlow aims to provide a unified platform for processing images, videos, audio, and documents.

The long-term goal is to help content creators automate repetitive media preparation tasks.

## Current Functionality

- FastAPI application factory with configurable application metadata and debug mode.
- Environment-based configuration using Pydantic Settings.
- Health-check endpoint and automatically generated API documentation.
- Image validation for JPEG, PNG, and WebP files.
- In-memory image conversion between JPEG, PNG, and WebP using Pillow.
- Conversion options for JPEG/WebP quality and background color when flattening transparency for JPEG.
- Domain-specific exceptions for invalid images, unsupported formats, oversized images, and conversion failures.
- Automated tests, code quality checks, and static type checking.

## Planned Features

- [x] Image format conversion core (Python service; no HTTP endpoint yet)
- [ ] Video format conversion
- [ ] Audio processing
- [ ] Document conversion
- [ ] Batch file processing
- [ ] REST API endpoint for image conversion and other media processing

The image conversion core is implemented, but the end-user upload/download API, frontend, and other media workflows are not yet available.

## Tech Stack

- **Python 3.12+** — Programming language
- **FastAPI** — Web API framework
- **Uvicorn** — ASGI server
- **Pydantic Settings** — Application configuration
- **Pillow** — Image decoding, validation, and conversion
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

### Image Conversion Core (DEV-004)

The conversion core is a Python service, **not yet an HTTP endpoint**. It supports all nine source/target combinations of JPEG, PNG, and WebP, including re-encoding to the same format.

**Input validation** is performed by `creatorflow.services.image_validator.validate_image(data)`. It accepts image bytes, detects the actual format using Pillow, verifies and decodes the image, and rejects:

- Empty, non-byte, or corrupt image data.
- Unsupported formats and animated images.
- Files larger than **10 MiB**.
- Images larger than **25,000,000 pixels**.

The limits apply to input files and image dimensions; they do not represent a fixed limit on decoded memory usage or output size.

**Conversion** is provided by `creatorflow.services.image_converter.PillowImageConverter`, which implements the `ImageConverter` protocol. Its `convert_image(data, options)` method returns a `ConversionResult` containing the output bytes, `ImageFormat`, and MIME type. All processing is performed in memory.

```python
from creatorflow.domain.image import ConversionOptions, ImageFormat
from creatorflow.services.image_converter import PillowImageConverter

with open("input.png", "rb") as source:
    image_bytes = source.read()

result = PillowImageConverter().convert_image(
    image_bytes,
    ConversionOptions(
        target_format=ImageFormat.JPEG,
        quality=85,
        background_color=(255, 255, 255),
    ),
)

with open("output.jpg", "wb") as destination:
    destination.write(result.data)

assert result.content_type == "image/jpeg"
```

This example uses local files only to demonstrate how to call the service. The converter itself does not write files.

| Option | Default | Behavior |
| --- | --- | --- |
| `target_format` | Required | `ImageFormat.JPEG`, `.PNG`, or `.WEBP` |
| `quality` | `85` | Integer from 1 to 100; used for JPEG and WebP, ignored for PNG |
| `background_color` | `(255, 255, 255)` | RGB tuple used to flatten transparent images when saving JPEG |

PNG and WebP output preserve transparency when present; JPEG does not support transparency, so transparent pixels are composited over the configured background. The converter also handles palette, grayscale, and CMYK input modes where appropriate.

The service exposes domain exceptions from `creatorflow.domain.exceptions`:

| Exception | Meaning |
| --- | --- |
| `InvalidImageError` | Invalid, corrupt, or undecodable image |
| `UnsupportedImageFormatError` | Unsupported source format or animation |
| `ImageTooLargeError` | Input file or pixel limit exceeded |
| `InvalidConversionOptionsError` | Invalid conversion settings |
| `ImageConversionError` | Other conversion/encoding failure |

These are Python exceptions; HTTP status mapping is planned for DEV-005.

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
│       ├── domain/
│       │   ├── exceptions.py
│       │   └── image.py
│       ├── services/
│       │   ├── image_converter.py
│       │   └── image_validator.py
│       ├── utils/
│       │   └── filenames.py
│       ├── __init__.py
│       ├── main.py
│       └── py.typed
├── tests/
│   ├── api/
│   │   └── test_health.py
│   ├── domain/
│   │   └── test_image.py
│   ├── services/
│   │   ├── test_image_converter.py
│   │   └── test_image_validator.py
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
4. [x] DEV-004: Implement image domain contracts, validation, conversion, and unit tests.
5. [ ] DEV-005: Expose image conversion through a FastAPI upload/download endpoint.
6. [ ] Add batch processing and expand media-processing capabilities to video, audio, and documents.

## License

No license has been specified yet.
