# Theater Pose Estimation API — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a FastAPI server that accepts theater performance images and returns pose estimations (keypoint coordinates + annotated skeleton overlay) using YOLOv8-Pose.

**Architecture:** Simple monolith — FastAPI with synchronous YOLOv8-Pose inference. Model loaded at startup, swappable behind an abstract interface. Single endpoint returns keypoints JSON + optional annotated image.

**Tech Stack:** Python 3.13, FastAPI, Uvicorn, Scalar, Ultralytics (YOLOv8-Pose), Pydantic v2, pydantic-settings, Pillow, PyTorch (CUDA), python-multipart

---

### Task 1: Project Setup & Dependencies

**Files:**
- Create: `requirements.txt`
- Create: `app/__init__.py`
- Create: `app/api/__init__.py`
- Create: `app/api/routes/__init__.py`
- Create: `app/models/__init__.py`
- Create: `app/services/__init__.py`
- Create: `app/utils/__init__.py`

**Step 1: Initialize git repo**

```bash
cd C:/Users/f.nefzi/Desktop/Personal/Theater-Detection
git init
```

**Step 2: Create requirements.txt**

```
fastapi>=0.115.0
uvicorn[standard]>=0.34.0
ultralytics>=8.3.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
pillow>=11.0.0
python-multipart>=0.0.18
scalar-fastapi>=1.0.0
```

**Step 3: Create all `__init__.py` files**

Create empty `__init__.py` in: `app/`, `app/api/`, `app/api/routes/`, `app/models/`, `app/services/`, `app/utils/`

**Step 4: Create virtual environment and install dependencies**

```bash
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
```

**Step 5: Verify installation**

```bash
python -c "import fastapi; import ultralytics; import torch; print(f'FastAPI: {fastapi.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}')"
```

Expected: FastAPI version prints, CUDA available: True

**Step 6: Commit**

```bash
git add requirements.txt app/
git commit -m "chore: project setup with dependencies and package structure"
```

---

### Task 2: Configuration Module

**Files:**
- Create: `app/config.py`
- Create: `tests/__init__.py`
- Create: `tests/test_config.py`

**Step 1: Write the failing test**

```python
# tests/test_config.py
from app.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.model_name == "yolov8m-pose.pt"
    assert settings.device == "auto"
    assert settings.confidence_threshold == 0.5
    assert settings.max_image_size == 1920
    assert settings.max_file_size_mb == 10
    assert settings.allowed_extensions == {"jpg", "jpeg", "png", "webp"}
    assert settings.min_image_dimension == 64


def test_custom_settings_from_env(monkeypatch):
    monkeypatch.setenv("MODEL_NAME", "yolov8n-pose.pt")
    monkeypatch.setenv("CONFIDENCE_THRESHOLD", "0.7")
    settings = Settings()
    assert settings.model_name == "yolov8n-pose.pt"
    assert settings.confidence_threshold == 0.7
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_config.py -v`
Expected: FAIL — `ModuleNotFoundError` or `ImportError`

**Step 3: Write minimal implementation**

```python
# app/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = "yolov8m-pose.pt"
    device: str = "auto"  # "auto", "cpu", "cuda", "cuda:0"
    confidence_threshold: float = 0.5
    max_image_size: int = 1920  # max dimension in px, images resized if larger
    max_file_size_mb: int = 10
    allowed_extensions: set[str] = {"jpg", "jpeg", "png", "webp"}
    min_image_dimension: int = 64  # minimum width/height in px

    model_config = {"env_prefix": "", "case_sensitive": False}


def get_settings() -> Settings:
    return Settings()
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_config.py -v`
Expected: 2 passed

**Step 5: Commit**

```bash
git add app/config.py tests/
git commit -m "feat: add configuration module with env var support"
```

---

### Task 3: Pydantic Schemas

**Files:**
- Create: `app/models/schemas.py`
- Create: `tests/test_schemas.py`

**Step 1: Write the failing test**

```python
# tests/test_schemas.py
from app.models.schemas import Keypoint, Actor, PoseMetadata, PoseEstimationResponse


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
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_schemas.py -v`
Expected: FAIL — `ImportError`

**Step 3: Write minimal implementation**

```python
# app/models/schemas.py
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


class PoseMetadata(BaseModel):
    image_width: int
    image_height: int
    model: str
    inference_time_ms: float
    actor_count: int


class PoseEstimationResponse(BaseModel):
    image_id: str
    actors: list[Actor]
    annotated_image: str | None = None
    metadata: PoseMetadata
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_schemas.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add app/models/schemas.py tests/test_schemas.py
git commit -m "feat: add Pydantic schemas for pose estimation API"
```

---

### Task 4: Image Utilities

**Files:**
- Create: `app/utils/image.py`
- Create: `tests/test_image_utils.py`

**Step 1: Write the failing tests**

```python
# tests/test_image_utils.py
import io
import pytest
from PIL import Image
from app.utils.image import validate_image, resize_if_needed, image_to_base64


def _make_test_image(width: int, height: int, fmt: str = "PNG") -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def test_validate_image_valid():
    data = _make_test_image(640, 480, "PNG")
    img = validate_image(data, allowed_extensions={"png", "jpg"}, max_file_size_mb=10, min_dimension=64)
    assert img.size == (640, 480)


def test_validate_image_too_large():
    data = b"x" * (11 * 1024 * 1024)  # 11MB
    with pytest.raises(ValueError, match="File size"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_validate_image_too_small():
    data = _make_test_image(32, 32, "PNG")
    with pytest.raises(ValueError, match="too small"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_validate_image_invalid_format():
    data = b"not an image"
    with pytest.raises(ValueError, match="Could not open"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_resize_if_needed_no_resize():
    img = Image.new("RGB", (800, 600))
    result = resize_if_needed(img, max_size=1920)
    assert result.size == (800, 600)


def test_resize_if_needed_downscale():
    img = Image.new("RGB", (3840, 2160))
    result = resize_if_needed(img, max_size=1920)
    assert max(result.size) == 1920
    # Aspect ratio preserved
    assert result.size == (1920, 1080)


def test_image_to_base64():
    img = Image.new("RGB", (100, 100), color="blue")
    b64 = image_to_base64(img)
    assert isinstance(b64, str)
    assert len(b64) > 0
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_image_utils.py -v`
Expected: FAIL — `ImportError`

**Step 3: Write minimal implementation**

```python
# app/utils/image.py
import base64
import io

from PIL import Image


def validate_image(
    data: bytes,
    allowed_extensions: set[str],
    max_file_size_mb: int,
    min_dimension: int,
) -> Image.Image:
    max_bytes = max_file_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise ValueError(f"File size {len(data)} exceeds maximum {max_bytes} bytes")

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception:
        raise ValueError("Could not open image — unsupported or corrupt file")

    fmt = (img.format or "").lower()
    if fmt == "jpeg":
        fmt = "jpg"
    if fmt not in allowed_extensions and "jpg" not in allowed_extensions:
        # Also check by trying common mappings
        format_map = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp"}
        mapped = format_map.get(fmt, fmt)
        if mapped not in allowed_extensions:
            raise ValueError(f"Image format '{fmt}' not allowed. Allowed: {allowed_extensions}")

    w, h = img.size
    if w < min_dimension or h < min_dimension:
        raise ValueError(f"Image too small ({w}x{h}). Minimum dimension: {min_dimension}px")

    if img.mode != "RGB":
        img = img.convert("RGB")

    return img


def resize_if_needed(img: Image.Image, max_size: int) -> Image.Image:
    w, h = img.size
    if max(w, h) <= max_size:
        return img

    if w >= h:
        new_w = max_size
        new_h = int(h * (max_size / w))
    else:
        new_h = max_size
        new_w = int(w * (max_size / h))

    return img.resize((new_w, new_h), Image.LANCZOS)


def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")
```

**Step 4: Run tests to verify they pass**

Run: `python -m pytest tests/test_image_utils.py -v`
Expected: 7 passed

**Step 5: Commit**

```bash
git add app/utils/image.py tests/test_image_utils.py
git commit -m "feat: add image validation, resize, and base64 utilities"
```

---

### Task 5: Abstract PoseEstimator Interface

**Files:**
- Create: `app/services/base.py`
- Create: `tests/test_services_base.py`

**Step 1: Write the failing test**

```python
# tests/test_services_base.py
import pytest
from PIL import Image
from app.services.base import PoseEstimator, PoseResult


def test_pose_estimator_is_abstract():
    with pytest.raises(TypeError):
        PoseEstimator()


def test_pose_result_dataclass():
    result = PoseResult(actors=[], annotated_image=None, inference_time_ms=12.5)
    assert result.actors == []
    assert result.annotated_image is None
    assert result.inference_time_ms == 12.5


def test_concrete_implementation():
    class FakeEstimator(PoseEstimator):
        def load_model(self) -> None:
            pass

        def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
            return PoseResult(actors=[], annotated_image=None, inference_time_ms=0.0)

        @property
        def model_name(self) -> str:
            return "fake"

    estimator = FakeEstimator()
    estimator.load_model()
    result = estimator.predict(Image.new("RGB", (100, 100)))
    assert result.inference_time_ms == 0.0
    assert estimator.model_name == "fake"
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_services_base.py -v`
Expected: FAIL — `ImportError`

**Step 3: Write minimal implementation**

```python
# app/services/base.py
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from PIL import Image

from app.models.schemas import Actor


@dataclass
class PoseResult:
    actors: list[Actor] = field(default_factory=list)
    annotated_image: Image.Image | None = None
    inference_time_ms: float = 0.0


class PoseEstimator(ABC):
    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory."""
        ...

    @abstractmethod
    def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
        """Run pose estimation on an image and return results."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier string."""
        ...
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_services_base.py -v`
Expected: 3 passed

**Step 5: Commit**

```bash
git add app/services/base.py tests/test_services_base.py
git commit -m "feat: add abstract PoseEstimator interface with PoseResult"
```

---

### Task 6: YOLOv8 Pose Estimator Implementation

**Files:**
- Create: `app/services/yolo_estimator.py`
- Create: `tests/test_yolo_estimator.py`

**Step 1: Write the failing test**

```python
# tests/test_yolo_estimator.py
import pytest
from PIL import Image
from app.services.yolo_estimator import YoloPoseEstimator

# Note: These tests require the model to be downloaded.
# First run will download yolov8m-pose.pt (~52MB).


@pytest.fixture(scope="module")
def estimator():
    est = YoloPoseEstimator(model_name="yolov8m-pose.pt", device="cpu")
    est.load_model()
    return est


def test_model_name(estimator):
    assert estimator.model_name == "yolov8m-pose"


def test_predict_blank_image(estimator):
    """A blank image should return zero actors."""
    img = Image.new("RGB", (640, 480), color="white")
    result = estimator.predict(img, confidence_threshold=0.5)
    assert result.actors == []
    assert result.inference_time_ms > 0


def test_predict_returns_pose_result(estimator):
    """Smoke test — model runs without crashing on a real-sized image."""
    img = Image.new("RGB", (1280, 720), color="gray")
    result = estimator.predict(img, confidence_threshold=0.1)
    assert result.inference_time_ms > 0
    # annotated_image should be a PIL Image
    assert result.annotated_image is None or isinstance(result.annotated_image, Image.Image)
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_yolo_estimator.py -v`
Expected: FAIL — `ImportError`

**Step 3: Write minimal implementation**

```python
# app/services/yolo_estimator.py
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
            annotated_array = result.plot()
            annotated_image = Image.fromarray(annotated_array[..., ::-1])  # BGR to RGB

        return PoseResult(
            actors=actors,
            annotated_image=annotated_image,
            inference_time_ms=elapsed_ms,
        )
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_yolo_estimator.py -v`
Expected: 3 passed (first run will download the model)

**Step 5: Add `.gitignore` to exclude model weights**

```
# .gitignore
__pycache__/
*.pyc
venv/
.env
*.pt
*.onnx
```

**Step 6: Commit**

```bash
git add app/services/yolo_estimator.py tests/test_yolo_estimator.py .gitignore
git commit -m "feat: add YOLOv8 pose estimator implementation"
```

---

### Task 7: FastAPI App with Scalar Docs

**Files:**
- Create: `app/main.py`
- Create: `tests/test_main.py`

**Step 1: Write the failing test**

```python
# tests/test_main.py
from fastapi.testclient import TestClient


def test_app_starts():
    from app.main import app
    client = TestClient(app)
    # Health check — Scalar docs should be accessible
    response = client.get("/")
    assert response.status_code == 200


def test_scalar_docs():
    from app.main import app
    client = TestClient(app)
    response = client.get("/scalar")
    assert response.status_code == 200
```

**Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_main.py -v`
Expected: FAIL — `ImportError`

**Step 3: Write minimal implementation**

```python
# app/main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.config import get_settings
from app.services.yolo_estimator import YoloPoseEstimator

estimator: YoloPoseEstimator | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global estimator
    settings = get_settings()
    estimator = YoloPoseEstimator(
        model_name=settings.model_name,
        device=settings.device,
    )
    estimator.load_model()
    yield
    estimator = None


app = FastAPI(
    title="Theater Pose Estimation API",
    description="Pose estimation for theater performance analysis. Upload an image to detect actor poses.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Theater Pose Estimation API", "docs": "/scalar"}


@app.get("/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Theater Pose Estimation API",
    )


def get_estimator() -> YoloPoseEstimator:
    if estimator is None:
        raise RuntimeError("Model not initialized")
    return estimator
```

**Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_main.py -v`
Expected: 2 passed

**Step 5: Commit**

```bash
git add app/main.py tests/test_main.py
git commit -m "feat: add FastAPI app with Scalar docs and model lifespan"
```

---

### Task 8: Pose Estimation Endpoint

**Files:**
- Create: `app/api/routes/pose.py`
- Modify: `app/main.py` (register router)
- Create: `tests/test_pose_endpoint.py`

**Step 1: Write the failing test**

```python
# tests/test_pose_endpoint.py
import io
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def _make_test_image(width: int = 640, height: int = 480) -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def test_estimate_valid_image(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert "image_id" in data
    assert "actors" in data
    assert "metadata" in data
    assert data["metadata"]["model"] == "yolov8m-pose"


def test_estimate_without_annotated_image(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate?return_image=false",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["annotated_image"] is None


def test_estimate_custom_confidence(client):
    image_data = _make_test_image()
    response = client.post(
        "/api/v1/pose/estimate?confidence_threshold=0.9",
        files={"file": ("test.png", image_data, "image/png")},
    )
    assert response.status_code == 200


def test_estimate_no_file(client):
    response = client.post("/api/v1/pose/estimate")
    assert response.status_code == 422


def test_estimate_too_small_image(client):
    image_data = _make_test_image(32, 32)
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("tiny.png", image_data, "image/png")},
    )
    assert response.status_code == 400


def test_estimate_invalid_file(client):
    response = client.post(
        "/api/v1/pose/estimate",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert response.status_code == 400
```

**Step 2: Run tests to verify they fail**

Run: `python -m pytest tests/test_pose_endpoint.py -v`
Expected: FAIL — 404 (route not registered)

**Step 3: Write the endpoint**

```python
# app/api/routes/pose.py
import uuid

from fastapi import APIRouter, File, Query, UploadFile, HTTPException

from app.config import get_settings
from app.main import get_estimator
from app.models.schemas import PoseEstimationResponse, PoseMetadata
from app.utils.image import validate_image, resize_if_needed, image_to_base64

router = APIRouter(prefix="/api/v1/pose", tags=["Pose Estimation"])


@router.post("/estimate", response_model=PoseEstimationResponse)
async def estimate_pose(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, or WebP)"),
    confidence_threshold: float = Query(
        default=0.5, ge=0.0, le=1.0, description="Minimum detection confidence"
    ),
    return_image: bool = Query(
        default=True, description="Include annotated image in response"
    ),
):
    settings = get_settings()

    data = await file.read()

    try:
        image = validate_image(
            data,
            allowed_extensions=settings.allowed_extensions,
            max_file_size_mb=settings.max_file_size_mb,
            min_dimension=settings.min_image_dimension,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    original_width, original_height = image.size
    image = resize_if_needed(image, max_size=settings.max_image_size)

    estimator = get_estimator()
    result = estimator.predict(image, confidence_threshold=confidence_threshold)

    annotated_b64 = None
    if return_image and result.annotated_image is not None:
        annotated_b64 = image_to_base64(result.annotated_image)

    return PoseEstimationResponse(
        image_id=str(uuid.uuid4()),
        actors=result.actors,
        annotated_image=annotated_b64,
        metadata=PoseMetadata(
            image_width=original_width,
            image_height=original_height,
            model=estimator.model_name,
            inference_time_ms=round(result.inference_time_ms, 2),
            actor_count=len(result.actors),
        ),
    )
```

**Step 4: Register the router in main.py**

Add to `app/main.py` after the app is created:

```python
from app.api.routes.pose import router as pose_router

app.include_router(pose_router)
```

**Step 5: Run tests to verify they pass**

Run: `python -m pytest tests/test_pose_endpoint.py -v`
Expected: 6 passed

**Step 6: Commit**

```bash
git add app/api/routes/pose.py app/main.py tests/test_pose_endpoint.py
git commit -m "feat: add POST /api/v1/pose/estimate endpoint"
```

---

### Task 9: README & Research Documentation

**Files:**
- Create: `README.md`
- Create: `research/2026-03-13-model-selection.md`

**Step 1: Write README.md**

```markdown
# Theater Pose Estimation API

A pose estimation API designed for analyzing theater performances. Upload an image of a theater scene and get back actor pose keypoints and an annotated skeleton overlay.

## Purpose

This is a research project exploring computer vision applied to theater performances. The API serves as the foundation for a broader analysis platform that will include:

- Actor distance / spatial analysis
- Lighting analysis
- Choreography analysis
- Movement classification

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows Git Bash
# source venv/bin/activate    # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload

# Open API docs
# http://localhost:8000/scalar
```

## API Usage

### POST /api/v1/pose/estimate

Upload an image to get pose estimations.

**Parameters:**
- `file` (required): Image file (JPEG, PNG, or WebP)
- `confidence_threshold` (optional, default 0.5): Minimum detection confidence (0.0-1.0)
- `return_image` (optional, default true): Include annotated skeleton overlay image

**Example with curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/pose/estimate" \
  -F "file=@photo.jpg"
```

## Theater-Specific Considerations

### Occlusion
Costumes (capes, robes, large hats) and props (swords, umbrellas) can hide body parts. The API returns per-keypoint confidence scores — low confidence indicates the model is uncertain about that joint's position. Bounding box overlap may merge or split actors in dense scenes.

### Stage Lighting
Dramatic lighting (spotlights, blackouts, colored gels) creates high contrast that can degrade detection. The API accepts images as-is without preprocessing. For best results, use well-exposed images when possible.

### Unusual Poses
Theater involves exaggerated, non-natural poses (lying on floor, contorted positions, actors stacked). The model (YOLOv8-Pose, trained on COCO) is optimized for everyday poses — accuracy drops on extreme theatrical positions. Per-keypoint confidence scores help identify unreliable detections.

### Multi-Person Scenes
The API handles any number of actors, from solo performances to large ensemble scenes. In crowded scenes with overlapping actors, some detections may be missed or confused. Actor IDs are assigned per-image and are not tracked across images.

### Image Requirements
- **Formats:** JPEG, PNG, WebP
- **Max file size:** 10MB (configurable)
- **Min resolution:** 64x64 pixels
- **Large images:** Automatically resized to max 1920px to fit GPU memory (4GB VRAM)

## Model

Currently uses **YOLOv8m-Pose** (medium variant). Returns COCO 17-keypoint format:

nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder, left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee, right_knee, left_ankle, right_ankle

Future: MMPose integration for improved accuracy on challenging poses.

## Configuration

Environment variables:
- `MODEL_NAME` — Model file (default: `yolov8m-pose.pt`)
- `DEVICE` — Inference device: `auto`, `cpu`, `cuda` (default: `auto`)
- `CONFIDENCE_THRESHOLD` — Default confidence threshold (default: `0.5`)
- `MAX_IMAGE_SIZE` — Max image dimension in pixels (default: `1920`)
- `MAX_FILE_SIZE_MB` — Max upload size (default: `10`)

## Project Structure

```
├── app/
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Settings from env vars
│   ├── api/routes/        # API endpoint handlers
│   ├── models/schemas.py  # Pydantic request/response models
│   ├── services/          # Pose estimation implementations
│   └── utils/             # Image processing utilities
├── research/             # Research notes and findings
├── tests/                # Test suite
└── docs/plans/           # Design & implementation docs
```
```

**Step 2: Write research note on model selection**

```markdown
# Model Selection: YOLOv8-Pose vs Alternatives

**Date:** 2026-03-13

## Context

Selecting a pose estimation model for theater performance analysis. Key requirements:
- Multi-person detection (1 to 10+ actors)
- Handle unusual/exaggerated poses
- Fit in 4GB VRAM (RTX 3050 Laptop)
- Open license

## Models Evaluated

### MediaPipe
- Lightweight, runs on CPU
- **Rejected:** Poor multi-person support, struggles with unusual poses

### OpenPose (Carnegie Mellon)
- Very accurate multi-person detection
- **Rejected:** Heavy resource usage, restrictive commercial license

### MMPose (OpenMMLab)
- Flexible, many pretrained models, good accuracy
- Apache 2.0 license
- **Deferred:** More complex integration, planned as future upgrade for accuracy-critical scenarios

### YOLOv8-Pose (Ultralytics) — SELECTED
- Single-stage detection + pose estimation
- Handles multi-person well
- Fits 4GB VRAM
- Apache 2.0 license
- Model size variants (nano → medium) for tuning speed/accuracy

## Decision

Start with **YOLOv8m-Pose** (medium). Good balance of speed and accuracy. Architecture uses abstract interface so switching to MMPose later is a config change.

## Known Limitations for Theater
- Trained on COCO dataset (everyday poses) — accuracy drops on extreme theatrical positions
- Dense overlapping actors may cause missed detections
- Costumes/props cause occlusion and potential confusion
```

**Step 3: Commit**

```bash
git add README.md research/2026-03-13-model-selection.md
git commit -m "docs: add README with theater considerations and model selection research"
```

---

### Task 10: Final Integration Test & Run

**Files:**
- No new files

**Step 1: Run all tests**

```bash
python -m pytest tests/ -v
```

Expected: All tests pass

**Step 2: Start the server manually and verify**

```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000/scalar` in browser — Scalar docs should show the endpoint.

**Step 3: Test with curl**

```bash
curl -X POST "http://localhost:8000/api/v1/pose/estimate" \
  -F "file=@some_test_image.jpg"
```

Verify JSON response with expected structure.

**Step 4: Final commit**

```bash
git add -A
git commit -m "chore: final cleanup and integration verification"
```
