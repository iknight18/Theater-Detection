import numpy as np
from app.models.schemas import Actor, Keypoint
from app.utils.distance import compute_actor_distances


def _make_actor(actor_id: int, keypoints_xy: list[tuple[float, float]]) -> Actor:
    names = [
        "nose", "left_eye", "right_eye", "left_ear", "right_ear",
        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
        "left_wrist", "right_wrist", "left_hip", "right_hip",
        "left_knee", "right_knee", "left_ankle", "right_ankle",
    ]
    keypoints = [
        Keypoint(name=names[i], x=x, y=y, confidence=0.9)
        for i, (x, y) in enumerate(keypoints_xy)
    ]
    return Actor(id=actor_id, confidence=0.9, bbox=[0, 0, 100, 100], keypoints=keypoints)


def test_compute_distances_two_actors():
    kps_a = [(100.0, 100.0)] * 17
    kps_b = [(200.0, 100.0)] * 17
    actor_a = _make_actor(0, kps_a)
    actor_b = _make_actor(1, kps_b)
    depth_map = np.full((480, 640), 0.5, dtype=np.float32)
    distances = compute_actor_distances([actor_a, actor_b], depth_map)
    assert len(distances) == 1
    assert distances[0].actor_a == 0
    assert distances[0].actor_b == 1
    assert distances[0].distance > 0


def test_compute_distances_single_actor():
    kps = [(100.0, 100.0)] * 17
    actor = _make_actor(0, kps)
    depth_map = np.full((480, 640), 0.5, dtype=np.float32)
    distances = compute_actor_distances([actor], depth_map)
    assert distances == []


def test_compute_distances_finds_closest_keypoints():
    kps_a = [(100.0, 100.0)] * 17
    kps_a[10] = (180.0, 100.0)  # right_wrist close to actor 1
    kps_b = [(300.0, 100.0)] * 17
    kps_b[9] = (200.0, 100.0)  # left_wrist close to actor 0
    actor_a = _make_actor(0, kps_a)
    actor_b = _make_actor(1, kps_b)
    depth_map = np.full((480, 640), 0.5, dtype=np.float32)
    distances = compute_actor_distances([actor_a, actor_b], depth_map)
    assert distances[0].keypoint_a.name == "right_wrist"
    assert distances[0].keypoint_b.name == "left_wrist"
