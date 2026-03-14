import pytest
from unittest.mock import MagicMock, patch
from PIL import Image

from app.services.sahi_estimator import SahiPoseEstimator
from app.services.base import PoseResult


def test_sahi_estimator_init():
    """SahiPoseEstimator should accept a model path and device."""
    estimator = SahiPoseEstimator(model_path="yolov8m-pose.pt", device="cpu")
    assert estimator.model_path == "yolov8m-pose.pt"


def test_sahi_estimator_predict_returns_pose_result():
    """predict() should return a PoseResult with actors list."""
    estimator = SahiPoseEstimator(model_path="yolov8m-pose.pt", device="cpu")

    # Mock the internal SAHI detection to avoid loading a real model
    estimator._model = MagicMock()  # bypass "model not loaded" guard
    with patch.object(estimator, '_run_sliced_prediction') as mock_predict:
        mock_predict.return_value = PoseResult(actors=[], inference_time_ms=5.0)

        img = Image.new("RGB", (640, 480), "gray")
        result = estimator.predict(img, confidence_threshold=0.5)

        assert isinstance(result, PoseResult)
        assert isinstance(result.actors, list)
