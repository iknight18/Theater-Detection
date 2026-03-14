import time

from PIL import Image
from ultralytics import YOLO

from app.models.schemas import Actor, Keypoint
from app.services.base import PoseEstimator, PoseResult

COCO_KEYPOINT_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle",
]


class YoloPoseEstimator(PoseEstimator):
    def __init__(self, model_name: str = "yolov8m-pose.pt", device: str = "auto"):
        self._model_name = model_name
        self._device = device
        self._model: YOLO | None = None

    def load_model(self) -> None:
        self._model = YOLO(self._model_name)
        if self._device != "auto":
            self._model.to(self._device)

    @property
    def model_name(self) -> str:
        return self._model_name.replace(".pt", "")

    def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        start = time.perf_counter()
        results = self._model(image, conf=confidence_threshold, verbose=False)
        elapsed_ms = (time.perf_counter() - start) * 1000

        actors = []
        annotated_image = None

        if results and len(results) > 0:
            result = results[0]

            # Parse detections
            if result.keypoints is not None and result.boxes is not None:
                keypoints_data = result.keypoints.data.cpu().numpy()
                boxes_data = result.boxes.data.cpu().numpy()

                for actor_id, (kps, box) in enumerate(zip(keypoints_data, boxes_data)):
                    keypoints = []
                    for i, name in enumerate(COCO_KEYPOINT_NAMES):
                        if i < len(kps):
                            x, y, conf = float(kps[i][0]), float(kps[i][1]), float(kps[i][2])
                            keypoints.append(Keypoint(name=name, x=x, y=y, confidence=conf))

                    bbox = [float(box[0]), float(box[1]), float(box[2]), float(box[3])]
                    actor_conf = float(box[4])

                    actors.append(Actor(
                        id=actor_id,
                        confidence=actor_conf,
                        bbox=bbox,
                        keypoints=keypoints,
                    ))

            # Generate annotated image
            annotated_array = result.plot(line_width=1, labels=False, conf=False)
            annotated_image = Image.fromarray(annotated_array[..., ::-1])  # BGR to RGB

        return PoseResult(
            actors=actors,
            annotated_image=annotated_image,
            inference_time_ms=elapsed_ms,
        )
