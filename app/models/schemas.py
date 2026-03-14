from pydantic import BaseModel


class Keypoint(BaseModel):
    name: str
    x: float
    y: float
    confidence: float


class Actor(BaseModel):
    id: int
    confidence: float
    bbox: list[float]  # [x1, y1, x2, y2]
    keypoints: list[Keypoint]


class DistanceKeypoint(BaseModel):
    name: str
    x: float
    y: float
    depth: float


class ActorDistance(BaseModel):
    actor_a: int
    actor_b: int
    distance: float
    keypoint_a: DistanceKeypoint
    keypoint_b: DistanceKeypoint


class PoseMetadata(BaseModel):
    image_width: int
    image_height: int
    model: str
    inference_time_ms: float
    actor_count: int


class PoseEstimationResponse(BaseModel):
    image_id: str
    actors: list[Actor]
    distances: list[ActorDistance] | None = None
    annotated_image_url: str | None = None
    metadata: PoseMetadata
