import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _make_test_image(width: int = 640, height: int = 480) -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_estimate_valid_image(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "image_id" in data
    assert "actors" in data
    assert "metadata" in data
    assert data["metadata"]["model"] == "yolov8m-pose"


def test_estimate_without_annotated_image(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate?return_image=false",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["annotated_image"] is None


def test_estimate_custom_confidence(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate?confidence_threshold=0.9",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200


def test_estimate_no_file(client):
    response = client.post("/api/v1/pose/estimate")
    assert response.status_code == 422


def test_estimate_too_small_image(client):
    image_data = _make_test_image(32, 32)
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("tiny.png", image_data, "image/png")},
    )
    assert response.status_code == 400


def test_estimate_invalid_file(client):
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400
