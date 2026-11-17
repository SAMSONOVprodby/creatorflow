from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from creatorflow.core.config import Settings
from creatorflow.main import create_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app(Settings(environment="testing", _env_file=None))

    with TestClient(app) as test_client:
        yield test_client
