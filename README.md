# CreatorFlow

**CreatorFlow** is a Python-based media processing project designed to simplify file conversion and content preparation workflows for creators.

> 🚧 Project status: Early development.

## Overview

CreatorFlow aims to provide a unified platform for processing images, videos, audio, and documents.

The long-term goal is to help content creators automate repetitive media preparation tasks.

## Planned Features

- [ ] Image format conversion
- [ ] Video format conversion
- [ ] Audio processing
- [ ] Document conversion
- [ ] Batch file processing
- [ ] REST API for media processing

These features are planned and are not yet available as a complete application.

## Tech Stack

- **Python 3.12** — Programming language
- **uv** — Dependency and environment management
- **pytest** — Automated testing
- **Ruff** — Linting and formatting
- **mypy** — Static type checking

## Getting Started

### Prerequisites

- Python 3.12+
- uv
- Git

### Installation

Clone the repository:

```bash
git clone https://github.com/SAMSONOVprodby/creatorflow.git
cd creatorflow
```

Install dependencies:

```bash
uv sync
```

### Development

Run the test suite:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=creatorflow --cov-report=term-missing
```

Check code quality:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy src
```

Automatically format code:

```bash
uv run ruff format .
```

## Project Structure

```text
creatorflow/
├── src/
│   └── creatorflow/
│       ├── __init__.py
│       └── utils/
├── tests/
├── pyproject.toml
├── uv.lock
└── README.md
```

The structure will evolve as new modules are introduced.

## Roadmap

The initial development milestones are:

1. Establish project tooling and testing.
2. Implement reusable file-processing utilities.
3. Introduce the first media conversion functionality.
4. Add batch processing.
5. Build an API layer.

## License

No license has been specified yet.
