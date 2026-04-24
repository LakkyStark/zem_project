from fastapi.testclient import TestClient

from buildlaw_api.main import app


def test_openapi_json() -> None:
    client = TestClient(app)
    r = client.get("/openapi.json")
    assert r.status_code == 200
    data = r.json()
    assert data["info"]["title"] == "BuildLaw AI API"
    assert "/v1/auth/login" in data["paths"]
