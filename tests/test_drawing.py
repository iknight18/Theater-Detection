import numpy as np
from PIL import Image
from app.models.schemas import Actor, ActorDistance, DistanceKeypoint, Keypoint
from app.utils.drawing import draw_distance_lines, draw_pose_on_image


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


def _make_actor(actor_id: int, x_offset: float = 0) -> Actor:
    """Create a test actor with all 17 COCO keypoints."""
    keypoint_positions = [
        ("nose", 100, 50), ("left_eye", 95, 45), ("right_eye", 105, 45),
        ("left_ear", 90, 50), ("right_ear", 110, 50),
        ("left_shoulder", 80, 80), ("right_shoulder", 120, 80),
        ("left_elbow", 70, 120), ("right_elbow", 130, 120),
        ("left_wrist", 65, 150), ("right_wrist", 135, 150),
        ("left_hip", 85, 160), ("right_hip", 115, 160),
        ("left_knee", 80, 220), ("right_knee", 120, 220),
        ("left_ankle", 80, 280), ("right_ankle", 120, 280),
    ]
    keypoints = [
        Keypoint(name=name, x=x + x_offset, y=y, confidence=0.9)
        for name, x, y in keypoint_positions
    ]
    return Actor(
        id=actor_id,
        confidence=0.95,
        bbox=[60 + x_offset, 40, 140 + x_offset, 290],
        keypoints=keypoints,
    )


def test_draw_pose_on_image_returns_image():
    img = Image.new("RGB", (640, 480), color="black")
    actors = [_make_actor(0)]
    result = draw_pose_on_image(img, actors)
    assert isinstance(result, Image.Image)
    assert result.size == (640, 480)


def test_draw_pose_on_image_draws_something():
    img = Image.new("RGB", (640, 480), color="black")
    actors = [_make_actor(0)]
    result = draw_pose_on_image(img, actors)
    result_arr = np.array(result)
    original_arr = np.array(img)
    assert not np.array_equal(original_arr, result_arr)


def test_draw_pose_on_image_empty_actors():
    img = Image.new("RGB", (640, 480), color="black")
    result = draw_pose_on_image(img, [])
    assert isinstance(result, Image.Image)
    # Should return unchanged image
    assert np.array_equal(np.array(img), np.array(result))


def test_draw_pose_on_image_with_scale():
    """When inference was on a resized image, coords must be scaled back."""
    img = Image.new("RGB", (1920, 1080), color="black")
    actors = [_make_actor(0)]
    # scale_x=2.0, scale_y=2.0 means inference was at half resolution
    result = draw_pose_on_image(img, actors, scale_x=2.0, scale_y=2.0)
    assert isinstance(result, Image.Image)
    assert result.size == (1920, 1080)
