# tests/test_main.py
from fastapi.testclient import TestClient


def test_app_starts():
    from app.main import app
    client = TestClient(app)
    # Health check — Scalar docs should be accessible
    response = client.get("/")
    assert response.status_code == 200


def test_scalar_docs():
    from app.main import app
    client = TestClient(app)
    response = client.get("/scalar")
    assert response.status_code == 200
