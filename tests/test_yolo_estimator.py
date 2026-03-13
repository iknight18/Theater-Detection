import pytest
from PIL import Image
from app.services.yolo_estimator import YoloPoseEstimator

# Note: These tests require the model to be downloaded.
# First run will download yolov8m-pose.pt (~52MB).


@pytest.fixture(scope="module")
def estimator():
    est = YoloPoseEstimator(model_name="yolov8m-pose.pt", device="cpu")
    est.load_model()
    return est


def test_model_name(estimator):
    assert estimator.model_name == "yolov8m-pose"


def test_predict_blank_image(estimator):
    """A blank image should return zero actors."""
    img = Image.new("RGB", (640, 480), color="white")
    result = estimator.predict(img, confidence_threshold=0.5)
    assert result.actors == []
    assert result.inference_time_ms > 0


def test_predict_returns_pose_result(estimator):
    """Smoke test — model runs without crashing on a real-sized image."""
    img = Image.new("RGB", (1280, 720), color="gray")
    result = estimator.predict(img, confidence_threshold=0.1)
    assert result.inference_time_ms > 0
    # annotated_image should be a PIL Image
    assert result.annotated_image is None or isinstance(result.annotated_image, Image.Image)
