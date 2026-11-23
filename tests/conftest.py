import io
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from creatorflow.core.config import Settings
from creatorflow.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(Settings(environment="testing", _env_file=None))

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def valid_png_bytes() -> bytes:
    with io.BytesIO() as buffer, Image.new("RGB", (8, 8), "red") as image:
        image.save(buffer, format="PNG")
        return buffer.getvalue()
