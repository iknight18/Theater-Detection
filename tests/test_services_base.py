import pytest
from PIL import Image
from app.services.base import PoseEstimator, PoseResult


def test_pose_estimator_is_abstract():
    with pytest.raises(TypeError):
        PoseEstimator()


def test_pose_result_dataclass():
    result = PoseResult(actors=[], annotated_image=None, inference_time_ms=12.5)
    assert result.actors == []
    assert result.annotated_image is None
    assert result.inference_time_ms == 12.5


def test_concrete_implementation():
    class FakeEstimator(PoseEstimator):
        def load_model(self) -> None:
            pass

        def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
            return PoseResult(actors=[], annotated_image=None, inference_time_ms=0.0)

        @property
        def model_name(self) -> str:
            return "fake"

    estimator = FakeEstimator()
    estimator.load_model()
    result = estimator.predict(Image.new("RGB", (100, 100)))
    assert result.inference_time_ms == 0.0
    assert estimator.model_name == "fake"
