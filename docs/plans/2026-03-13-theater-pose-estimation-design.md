# Theater Pose Estimation API — Design Document

**Date:** 2026-03-13
**Status:** Approved

## Overview

A Python server that accepts theater performance images and returns pose estimations (keypoint coordinates + annotated skeleton overlay). This is the foundation for a broader theater performance analysis platform that will later include actor distance calculations, lighting analysis, and more.

## API Design

### Endpoint

```
POST /api/v1/pose/estimate
```

**Input:** Multipart form upload (JPEG, PNG, WebP)

**Query Parameters:**
- `confidence_threshold` (float, default 0.5) — minimum detection confidence
- `return_image` (bool, default true) — whether to include annotated image in response

**Response:**
```json
{
  "image_id": "uuid",
  "actors": [
    {
      "id": 0,
      "confidence": 0.92,
      "bbox": [x1, y1, x2, y2],
      "keypoints": [
        {"name": "nose", "x": 312.5, "y": 148.2, "confidence": 0.95},
        {"name": "left_shoulder", "x": 290.1, "y": 210.4, "confidence": 0.88}
      ]
    }
  ],
  "annotated_image": "<base64 encoded PNG with skeleton overlay>",
  "metadata": {
    "image_width": 1920,
    "image_height": 1080,
    "model": "yolov8m-pose",
    "inference_time_ms": 45.2,
    "actor_count": 3
  }
}
```

Uses COCO 17-keypoint format (nose, eyes, ears, shoulders, elbows, wrists, hips, knees, ankles).

## Architecture

**Approach:** Simple monolith (FastAPI + synchronous inference)

- Model loaded once at startup via FastAPI lifespan event
- Single Uvicorn worker process
- Swappable model via abstract `PoseEstimator` interface (YOLOv8 now, MMPose later)

### Project Structure

```
Theater-Detection/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, Scalar docs setup
│   ├── config.py             # Settings (model path, thresholds, etc.)
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── pose.py       # POST /api/v1/pose/estimate
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py        # Pydantic models (request/response)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── base.py           # Abstract PoseEstimator interface
│   │   └── yolo_estimator.py # YOLOv8 implementation
│   └── utils/
│       ├── __init__.py
│       └── image.py          # Image loading, validation, base64 encoding
├── research/                  # Research notes and findings
├── docs/
│   └── plans/
├── requirements.txt
└── README.md
```

## Model Choice

**Primary:** YOLOv8-Pose (medium variant — `yolov8m-pose`)

**Rationale:**
- Single-stage detection + pose in one pass (fast)
- Handles multi-person well out of the box
- Fits in 4GB VRAM (RTX 3050 Laptop)
- Apache 2.0 license, actively maintained
- Easy to tune via model size variants (nano → small → medium)

**Future upgrade:** MMPose with additional optimizations

## Edge Cases & Limitations

### Occlusion
- Costumes (capes, robes, large hats) hide keypoints — model returns low confidence for those joints. Surfaced clearly, not guessed.
- Props (swords, umbrellas, chairs) can confuse the detector — bounding box overlap may merge or split actors.

### Lighting
- Stage lighting is dramatic (spotlights, blackouts, colored gels). High contrast causes under/overexposure.
- No preprocessing for now — accept images as-is. Future enhancement: histogram equalization or similar.

### Unusual Poses
- Theater involves exaggerated, non-natural poses. YOLOv8 trained on COCO (mostly "normal" poses) — accuracy drops on extreme positions.
- Per-keypoint confidence scores let consumers decide what to trust. Low-confidence keypoints are flagged, not filtered.

### Multi-Person Confusion
- Crowd scenes with overlapping actors can cause missed detections.
- Actor IDs are arbitrary per-image (no tracking across images for now).

### Image Quality & Limits
- Accepted formats: JPEG, PNG, WebP
- Max file size: 10MB (configurable)
- Minimum resolution check
- High-res images (4K+) resized to max 1920px before inference to avoid OOM on 4GB VRAM

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn (ASGI server)
- Scalar (API docs)
- Ultralytics (YOLOv8-Pose)
- Pydantic v2 + pydantic-settings
- Pillow (image handling)
- PyTorch + torchvision (CUDA-enabled)
- python-multipart (file uploads)

## Future Considerations

- Video frame processing support
- Actor distance / spatial analysis
- Lighting analysis
- MMPose integration for improved accuracy
- Multiple Uvicorn workers for concurrency
- Image preprocessing pipeline for challenging lighting conditions
