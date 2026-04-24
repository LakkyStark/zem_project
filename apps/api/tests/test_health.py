from fastapi.testclient import TestClient

from buildlaw_api.main import app


def test_health() -> None:
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code in (200, 503)
