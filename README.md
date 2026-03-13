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
