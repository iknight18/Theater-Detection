import time

import numpy as np
from PIL import Image
from ultralytics import YOLO

from app.models.schemas import Actor, Keypoint
from app.services.base import PoseResult
from app.services.yolo_estimator import COCO_KEYPOINT_NAMES


class SahiPoseEstimator:
    def __init__(
        self,
        model_path: str = "yolov8m-pose.pt",
        device: str = "cpu",
        slice_size: int = 640,
        overlap_ratio: float = 0.25,
    ):
        self.model_path = model_path
        self.device = device
        self.slice_size = slice_size
        self.overlap_ratio = overlap_ratio
        self._model: YOLO | None = None

    def load_model(self) -> None:
        self._model = YOLO(self.model_path)
        if self.device != "auto":
            self._model.to(self.device)

    def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self._run_sliced_prediction(image, confidence_threshold)

    def _run_sliced_prediction(
        self, image: Image.Image, confidence_threshold: float
    ) -> PoseResult:
        """Run YOLO on overlapping slices, merge results with NMS."""
        img_array = np.array(image)
        h, w = img_array.shape[:2]

        start = time.perf_counter()

        all_actors = []
        actor_id_counter = 0
        step = int(self.slice_size * (1 - self.overlap_ratio))

        for y0 in range(0, h, step):
            for x0 in range(0, w, step):
                x1 = min(x0 + self.slice_size, w)
                y1 = min(y0 + self.slice_size, h)
                tile = image.crop((x0, y0, x1, y1))

                results = self._model(tile, conf=confidence_threshold, verbose=False)
                if not results or len(results) == 0:
                    continue

                result = results[0]
                if result.keypoints is None or result.boxes is None:
                    continue

                kps_data = result.keypoints.data.cpu().numpy()
                boxes_data = result.boxes.data.cpu().numpy()

                for kps, box in zip(kps_data, boxes_data):
                    keypoints = []
                    for i, name in enumerate(COCO_KEYPOINT_NAMES):
                        if i < len(kps):
                            x, y, conf = float(kps[i][0]), float(kps[i][1]), float(kps[i][2])
                            keypoints.append(Keypoint(
                                name=name, x=x + x0, y=y + y0, confidence=conf
                            ))

                    bbox = [
                        float(box[0]) + x0, float(box[1]) + y0,
                        float(box[2]) + x0, float(box[3]) + y0,
                    ]
                    actor_conf = float(box[4])

                    all_actors.append(Actor(
                        id=actor_id_counter,
                        confidence=actor_conf,
                        bbox=bbox,
                        keypoints=keypoints,
                    ))
                    actor_id_counter += 1

        # NMS to remove duplicate detections from overlapping tiles
        all_actors = self._nms_actors(all_actors, iou_threshold=0.5)

        # Re-assign sequential IDs after NMS
        for i, actor in enumerate(all_actors):
            actor.id = i

        elapsed_ms = (time.perf_counter() - start) * 1000
        return PoseResult(actors=all_actors, inference_time_ms=elapsed_ms)

    @staticmethod
    def _nms_actors(actors: list[Actor], iou_threshold: float) -> list[Actor]:
        """Non-maximum suppression on actor bounding boxes."""
        if len(actors) <= 1:
            return actors

        boxes = np.array([a.bbox for a in actors])
        scores = np.array([a.confidence for a in actors])

        x1, y1, x2, y2 = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)

        order = scores.argsort()[::-1]
        keep = []

        while len(order) > 0:
            i = order[0]
            keep.append(i)

            if len(order) == 1:
                break

            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            inter = np.maximum(0.0, xx2 - xx1) * np.maximum(0.0, yy2 - yy1)
            iou = inter / (areas[i] + areas[order[1:]] - inter)

            remaining = np.where(iou <= iou_threshold)[0]
            order = order[remaining + 1]

        return [actors[i] for i in keep]
