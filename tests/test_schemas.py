from app.models.schemas import (
    Keypoint,
    Actor,
    PoseMetadata,
    PoseEstimationResponse,
    DistanceKeypoint,
    ActorDistance,
)


def test_keypoint_model():
    kp = Keypoint(name="nose", x=312.5, y=148.2, confidence=0.95)
    assert kp.name == "nose"
    assert kp.x == 312.5
    assert kp.confidence == 0.95


def test_actor_model():
    kp = Keypoint(name="nose", x=100.0, y=200.0, confidence=0.9)
    actor = Actor(id=0, confidence=0.92, bbox=[10.0, 20.0, 300.0, 400.0], keypoints=[kp])
    assert actor.id == 0
    assert len(actor.keypoints) == 1
    assert len(actor.bbox) == 4


def test_pose_estimation_response():
    kp = Keypoint(name="nose", x=100.0, y=200.0, confidence=0.9)
    actor = Actor(id=0, confidence=0.92, bbox=[10.0, 20.0, 300.0, 400.0], keypoints=[kp])
    metadata = PoseMetadata(
        image_width=1920,
        image_height=1080,
        model="yolov8m-pose",
        inference_time_ms=45.2,
        actor_count=1,
    )
    response = PoseEstimationResponse(
        image_id="test-uuid",
        actors=[actor],
        annotated_image=None,
        metadata=metadata,
    )
    assert response.image_id == "test-uuid"
    assert response.metadata.actor_count == 1
    assert response.annotated_image is None


def test_actor_distance_schema():
    kp_a = DistanceKeypoint(name="right_wrist", x=300.0, y=200.0, depth=0.45)
    kp_b = DistanceKeypoint(name="left_wrist", x=350.0, y=210.0, depth=0.48)
    dist = ActorDistance(
        actor_a=0,
        actor_b=1,
        distance=127.4,
        keypoint_a=kp_a,
        keypoint_b=kp_b,
    )
    assert dist.actor_a == 0
    assert dist.keypoint_a.depth == 0.45
    assert dist.distance == 127.4
