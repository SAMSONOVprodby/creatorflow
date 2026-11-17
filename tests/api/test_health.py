from fastapi.testclient import TestClient


def test_health_status_code(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200


def test_health_response_body(client: TestClient) -> None:
    response = client.get("/health")

    assert response.json() == {"status": "ok"}


def test_health_unknown_endpoint(client: TestClient) -> None:
    response = client.get("/unknown")

    assert response.status_code == 404


def test_health_method_not_allowed(client: TestClient) -> None:
    response = client.post("/health")

    assert response.status_code == 405
