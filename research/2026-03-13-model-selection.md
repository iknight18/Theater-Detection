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
