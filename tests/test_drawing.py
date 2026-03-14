import numpy as np
from PIL import Image
from app.models.schemas import ActorDistance, DistanceKeypoint
from app.utils.drawing import draw_distance_lines


def test_draw_distance_lines_returns_image():
    img = Image.new("RGB", (640, 480), color="black")
    distances = [
        ActorDistance(
            actor_a=0,
            actor_b=1,
            distance=127.4,
            keypoint_a=DistanceKeypoint(name="right_wrist", x=100, y=100, depth=0.5),
            keypoint_b=DistanceKeypoint(name="left_wrist", x=200, y=200, depth=0.5),
        )
    ]
    result = draw_distance_lines(img, distances)
    assert isinstance(result, Image.Image)
    assert result.size == (640, 480)


def test_draw_distance_lines_modifies_image():
    img = Image.new("RGB", (640, 480), color="black")
    original_data = np.array(img).copy()
    distances = [
        ActorDistance(
            actor_a=0,
            actor_b=1,
            distance=50.0,
            keypoint_a=DistanceKeypoint(name="nose", x=100, y=100, depth=0.5),
            keypoint_b=DistanceKeypoint(name="nose", x=300, y=300, depth=0.5),
        )
    ]
    result = draw_distance_lines(img, distances)
    result_data = np.array(result)
    assert not np.array_equal(original_data, result_data)


def test_draw_distance_lines_empty_list():
    img = Image.new("RGB", (640, 480), color="black")
    result = draw_distance_lines(img, [])
    assert isinstance(result, Image.Image)
