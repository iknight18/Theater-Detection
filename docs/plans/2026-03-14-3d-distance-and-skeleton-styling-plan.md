# 3D Actor Distance & Skeleton Styling Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add 3D distance measurement between actors using monocular depth estimation, a `show_distances` feature flag, thinner skeletons, and remove confidence/label annotations.

**Architecture:** A new `DepthEstimator` service wraps Depth Anything V2 Small. When `show_distances=true`, the depth map is computed, keypoints become 3D, and closest-keypoint distances are calculated per actor pair. Distance lines are drawn on the annotated image via OpenCV. Skeleton styling uses `result.plot()` parameters.

**Tech Stack:** Depth Anything V2 (transformers + torch), OpenCV, existing FastAPI + YOLOv8 stack.

---

### Task 1: Add `show_distances` config setting

**Files:**
- Modify: `app/config.py:4-11`
- Test: `tests/test_config.py`

**Step 1: Write the failing test**

Add to `tests/test_config.py`:

```python
def test_show_distances_default():
    settings = Settings()
    assert settings.show_distances is False
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_config.py::test_show_distances_default -v`
Expected: FAIL with `AttributeError`

**Step 3: Write minimal implementation**

In `app/config.py`, add to the `Settings` class after `min_image_dimension`:

```python
    show_distances: bool = False
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_config.py::test_show_distances_default -v`
Expected: PASS

**Step 5: Commit**

```bash
git add app/config.py tests/test_config.py
git commit -m "feat: add show_distances config setting"
```

---

### Task 2: Fix skeleton styling — thinner lines, no labels, no confidence

**Files:**
- Modify: `app/services/yolo_estimator.py:69`

**Step 1: Make the change**

In `app/services/yolo_estimator.py`, replace line 69:

```python
            annotated_array = result.plot()
```

with:

```python
            annotated_array = result.plot(line_width=1, labels=False, conf=False)
```

**Step 2: Run existing tests to verify nothing breaks**

Run: `pytest tests/test_yolo_estimator.py -v`
Expected: All PASS

**Step 3: Commit**

```bash
git add app/services/yolo_estimator.py
git commit -m "style: thinner skeleton lines, remove labels and confidence annotations"
```

---

### Task 3: Add distance-related schemas

**Files:**
- Modify: `app/models/schemas.py`
- Test: `tests/test_schemas.py`

**Step 1: Write the failing test**

Add to `tests/test_schemas.py`:

```python
from app.models.schemas import DistanceKeypoint, ActorDistance


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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_schemas.py::test_actor_distance_schema -v`
Expected: FAIL with `ImportError`

**Step 3: Write minimal implementation**

Add to `app/models/schemas.py` before `PoseMetadata`:

```python
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
```

Also add `distances` to `PoseEstimationResponse`:

```python
class PoseEstimationResponse(BaseModel):
    image_id: str
    actors: list[Actor]
    distances: list[ActorDistance] | None = None
    annotated_image_url: str | None = None
    metadata: PoseMetadata
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_schemas.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add app/models/schemas.py tests/test_schemas.py
git commit -m "feat: add ActorDistance and DistanceKeypoint schemas"
```

---

### Task 4: Create DepthEstimator service

**Files:**
- Create: `app/services/depth_estimator.py`
- Test: `tests/test_depth_estimator.py`

**Step 1: Write the failing test**

Create `tests/test_depth_estimator.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_depth_estimator.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Add dependency**

Add to `requirements.txt`:

```
transformers>=4.40.0
```

Note: `torch` is already installed as a dependency of `ultralytics`.

**Step 4: Install dependency**

Run: `pip install transformers>=4.40.0`

**Step 5: Write minimal implementation**

Create `app/services/depth_estimator.py`:

```python
import numpy as np
import torch
from PIL import Image
from transformers import pipeline


class DepthEstimator:
    def __init__(self, device: str = "auto"):
        self._device = device
        self._pipe = None

    def load_model(self) -> None:
        device_arg = self._resolve_device()
        self._pipe = pipeline(
            task="depth-estimation",
            model="depth-anything/Depth-Anything-V2-Small-hf",
            device=device_arg,
        )

    def _resolve_device(self) -> str:
        if self._device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return self._device

    def estimate(self, image: Image.Image) -> np.ndarray:
        if self._pipe is None:
            raise RuntimeError("Depth model not loaded. Call load_model() first.")

        result = self._pipe(image)
        depth_map = np.array(result["depth"], dtype=np.float32)

        # Normalize to 0-1 range
        d_min, d_max = depth_map.min(), depth_map.max()
        if d_max - d_min > 0:
            depth_map = (depth_map - d_min) / (d_max - d_min)
        else:
            depth_map = np.zeros_like(depth_map)

        return depth_map
```

**Step 6: Run test to verify it passes**

Run: `pytest tests/test_depth_estimator.py -v`
Expected: All PASS (first run will download the model)

**Step 7: Commit**

```bash
git add app/services/depth_estimator.py tests/test_depth_estimator.py requirements.txt
git commit -m "feat: add DepthEstimator service using Depth Anything V2 Small"
```

---

### Task 5: Create distance calculation utility

**Files:**
- Create: `app/utils/distance.py`
- Test: `tests/test_distance.py`

**Step 1: Write the failing test**

Create `tests/test_distance.py`:

```python
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
    # Actor 0 at left side, actor 1 at right side
    kps_a = [(100.0, 100.0)] * 17
    kps_b = [(200.0, 100.0)] * 17
    actor_a = _make_actor(0, kps_a)
    actor_b = _make_actor(1, kps_b)

    # Flat depth map (all same depth)
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
    # Actor 0: most keypoints at x=100, but right_wrist (index 10) at x=180
    kps_a = [(100.0, 100.0)] * 17
    kps_a[10] = (180.0, 100.0)  # right_wrist close to actor 1

    # Actor 1: most keypoints at x=300, but left_wrist (index 9) at x=200
    kps_b = [(300.0, 100.0)] * 17
    kps_b[9] = (200.0, 100.0)  # left_wrist close to actor 0

    actor_a = _make_actor(0, kps_a)
    actor_b = _make_actor(1, kps_b)

    depth_map = np.full((480, 640), 0.5, dtype=np.float32)
    distances = compute_actor_distances([actor_a, actor_b], depth_map)

    assert distances[0].keypoint_a.name == "right_wrist"
    assert distances[0].keypoint_b.name == "left_wrist"
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_distance.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

Create `app/utils/distance.py`:

```python
from itertools import combinations
import math

import numpy as np

from app.models.schemas import Actor, ActorDistance, DistanceKeypoint


def compute_actor_distances(
    actors: list[Actor],
    depth_map: np.ndarray,
) -> list[ActorDistance]:
    if len(actors) < 2:
        return []

    h, w = depth_map.shape
    distances = []

    for a, b in combinations(actors, 2):
        best_dist = float("inf")
        best_kp_a = None
        best_kp_b = None

        for kp_a in a.keypoints:
            if kp_a.confidence < 0.3:
                continue
            ax, ay = int(min(max(kp_a.x, 0), w - 1)), int(min(max(kp_a.y, 0), h - 1))
            a_depth = float(depth_map[ay, ax])

            for kp_b in b.keypoints:
                if kp_b.confidence < 0.3:
                    continue
                bx, by = int(min(max(kp_b.x, 0), w - 1)), int(min(max(kp_b.y, 0), h - 1))
                b_depth = float(depth_map[by, bx])

                dist = math.sqrt(
                    (kp_a.x - kp_b.x) ** 2
                    + (kp_a.y - kp_b.y) ** 2
                    + ((a_depth - b_depth) * max(w, h)) ** 2
                )

                if dist < best_dist:
                    best_dist = dist
                    best_kp_a = DistanceKeypoint(
                        name=kp_a.name, x=kp_a.x, y=kp_a.y, depth=a_depth,
                    )
                    best_kp_b = DistanceKeypoint(
                        name=kp_b.name, x=kp_b.x, y=kp_b.y, depth=b_depth,
                    )

        if best_kp_a is not None and best_kp_b is not None:
            distances.append(ActorDistance(
                actor_a=a.id,
                actor_b=b.id,
                distance=round(best_dist, 2),
                keypoint_a=best_kp_a,
                keypoint_b=best_kp_b,
            ))

    return distances
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_distance.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add app/utils/distance.py tests/test_distance.py
git commit -m "feat: add compute_actor_distances utility for 3D closest-keypoint distances"
```

---

### Task 6: Create distance overlay drawing utility

**Files:**
- Create: `app/utils/drawing.py`
- Test: `tests/test_drawing.py`

**Step 1: Write the failing test**

Create `tests/test_drawing.py`:

```python
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
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/test_drawing.py -v`
Expected: FAIL with `ModuleNotFoundError`

**Step 3: Write minimal implementation**

Create `app/utils/drawing.py`:

```python
import cv2
import numpy as np
from PIL import Image

from app.models.schemas import ActorDistance


def draw_distance_lines(
    image: Image.Image,
    distances: list[ActorDistance],
) -> Image.Image:
    if not distances:
        return image

    img_array = np.array(image)
    # PIL is RGB, OpenCV expects BGR
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    for dist in distances:
        pt_a = (int(dist.keypoint_a.x), int(dist.keypoint_a.y))
        pt_b = (int(dist.keypoint_b.x), int(dist.keypoint_b.y))

        # Draw line
        cv2.line(img_bgr, pt_a, pt_b, (0, 255, 255), 1, cv2.LINE_AA)

        # Draw label at midpoint
        mid_x = (pt_a[0] + pt_b[0]) // 2
        mid_y = (pt_a[1] + pt_b[1]) // 2
        label = f"{dist.distance:.1f}"
        cv2.putText(
            img_bgr, label, (mid_x + 5, mid_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA,
        )

    # Convert back to RGB PIL Image
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/test_drawing.py -v`
Expected: All PASS

**Step 5: Commit**

```bash
git add app/utils/drawing.py tests/test_drawing.py
git commit -m "feat: add draw_distance_lines utility for annotating distance overlays"
```

---

### Task 7: Load DepthEstimator at startup

**Files:**
- Modify: `app/main.py:10-20`

**Step 1: Update lifespan to load depth model**

In `app/main.py`, add import at top:

```python
from app.services.depth_estimator import DepthEstimator
```

Update the `lifespan` function to also load the depth estimator:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    estimator = YoloPoseEstimator(
        model_name=settings.model_name,
        device=settings.device,
    )
    estimator.load_model()
    app.state.estimator = estimator

    depth_estimator = DepthEstimator(device=settings.device)
    depth_estimator.load_model()
    app.state.depth_estimator = depth_estimator

    yield
    app.state.estimator = None
    app.state.depth_estimator = None
```

**Step 2: Run existing tests to verify nothing breaks**

Run: `pytest tests/test_main.py -v`
Expected: All PASS

**Step 3: Commit**

```bash
git add app/main.py
git commit -m "feat: load DepthEstimator at startup alongside YOLOv8"
```

---

### Task 8: Wire up distance calculation in the API endpoint

**Files:**
- Modify: `app/api/routes/pose.py`

**Step 1: Update the endpoint**

In `app/api/routes/pose.py`, add imports:

```python
from app.utils.distance import compute_actor_distances
from app.utils.drawing import draw_distance_lines
```

Add `show_distances` query parameter to the endpoint function signature:

```python
    show_distances: bool = Query(
        default=False, description="Compute and display 3D distances between actors"
    ),
```

After `result = estimator.predict(...)` and before `image_id = ...`, add the distance logic:

```python
    distances = None
    if show_distances and len(result.actors) >= 2:
        depth_estimator = request.app.state.depth_estimator
        if depth_estimator is None:
            raise HTTPException(status_code=503, detail="Depth model not initialized")
        depth_map = depth_estimator.estimate(image)
        distances = compute_actor_distances(result.actors, depth_map)

        if result.annotated_image is not None and distances:
            result.annotated_image = draw_distance_lines(result.annotated_image, distances)
```

Update the response to include `distances`:

```python
    return PoseEstimationResponse(
        image_id=image_id,
        actors=result.actors,
        distances=distances,
        annotated_image_url=annotated_image_url,
        metadata=PoseMetadata(
            image_width=original_width,
            image_height=original_height,
            model=estimator.model_name,
            inference_time_ms=round(result.inference_time_ms, 2),
            actor_count=len(result.actors),
        ),
    )
```

**Step 2: Use config default for `show_distances`**

Update the query parameter default to use config:

```python
    show_distances: bool = Query(
        default=None, description="Compute and display 3D distances between actors"
    ),
```

Then resolve the default from config in the function body:

```python
    if show_distances is None:
        show_distances = settings.show_distances
```

**Step 3: Run full test suite**

Run: `pytest -v`
Expected: All PASS

**Step 4: Commit**

```bash
git add app/api/routes/pose.py
git commit -m "feat: wire up 3D distance calculation in pose estimation endpoint"
```

---

### Task 9: Manual integration test

**Step 1: Start the server**

Run: `uvicorn app.main:app --reload`

**Step 2: Test without distances**

Upload an image via the `/scalar` docs UI or curl:

```bash
curl -X POST "http://localhost:8000/api/v1/pose/estimate" -F "file=@test_image.jpg"
```

Verify: response has no `distances` field (or `null`), skeleton is thin, no labels/confidence.

**Step 3: Test with distances**

```bash
curl -X POST "http://localhost:8000/api/v1/pose/estimate?show_distances=true" -F "file=@test_image.jpg"
```

Verify: response includes `distances` array (if 2+ actors detected), annotated image has distance lines.

**Step 4: Commit any final adjustments**

```bash
git add -A
git commit -m "feat: complete 3D distance measurement integration"
```
