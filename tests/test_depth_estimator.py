import pytest
import numpy as np
from PIL import Image
from app.services.depth_estimator import DepthEstimator


@pytest.fixture(scope="module")
def depth_estimator():
    est = DepthEstimator()
    est.load_model()
    return est


def test_estimate_depth_returns_array(depth_estimator):
    img = Image.new("RGB", (640, 480), color="gray")
    depth_map = depth_estimator.estimate(img)
    assert isinstance(depth_map, np.ndarray)
    assert depth_map.shape == (480, 640)


def test_estimate_depth_values_range(depth_estimator):
    img = Image.new("RGB", (320, 240), color="white")
    depth_map = depth_estimator.estimate(img)
    assert depth_map.min() >= 0.0
    assert depth_map.max() <= 1.0
