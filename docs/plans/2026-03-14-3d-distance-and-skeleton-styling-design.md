# 3D Actor Distance & Skeleton Styling Design

## Overview

Four changes to the pose estimation system:
1. Calculate 3D distances between actors using monocular depth estimation
2. Add a `show_distances` feature flag (config + API query param)
3. Reduce skeleton stroke width
4. Remove confidence and "person" annotations from output images

## 1. 3D Distance Calculation

### Depth Model
- **Model:** Depth Anything V2 Small
- **Loading:** At startup, alongside YOLOv8, via a `DepthEstimator` service
- **VRAM:** ~1.5GB total for both models (fits RTX 3050 4GB)

### Distance Metric
- **Closest keypoint pair** between each actor pair
- For each pair of actors, find the two keypoints (one per actor) with minimum 3D Euclidean distance

### Flow
1. Image arrives → run YOLOv8-Pose (keypoints) + Depth Anything V2 (depth map)
2. Sample depth at each keypoint's (x, y) position
3. Each keypoint becomes 3D: (x, y, depth)
4. For each actor pair, compute pairwise keypoint distances, return the minimum

### Response Schema Addition
```json
{
  "distances": [
    {
      "actor_a": 0,
      "actor_b": 1,
      "distance": 127.4,
      "keypoint_a": {"name": "right_wrist", "x": 300, "y": 200, "depth": 0.45},
      "keypoint_b": {"name": "left_wrist", "x": 350, "y": 210, "depth": 0.48}
    }
  ]
}
```

**Note:** Distances are in relative units (not meters) since monocular depth is scale-ambiguous. Useful for comparing relative proximity between actors.

## 2. Display Flag

### Config (`config.py`)
```python
show_distances: bool = False
```

### API Query Parameter
`show_distances` (bool, default from config) on `POST /api/v1/pose/estimate`

### Behavior
- **`show_distances=true`:** Depth model runs, `distances` array in response, distance lines drawn on annotated image
- **`show_distances=false`:** Depth model not invoked (but stays loaded), no `distances` field, no distance lines on image

## 3. Skeleton Styling & Annotation Removal

### Change
Replace `result.plot()` with:
```python
result.plot(line_width=1, labels=False, conf=False)
```

This:
- Reduces skeleton line thickness to 1px
- Removes "person" class labels
- Removes confidence score annotations

### Distance Overlay (when enabled)
- After `result.plot()`, draw lines between closest keypoint pairs using OpenCV
- Small distance value label at the line midpoint

## Approach Rationale

- **Depth Anything V2 Small** over MiDaS: better accuracy, fits VRAM
- **Separate DepthEstimator service:** follows existing service pattern, clean separation, testable
- **Always-loaded depth model:** avoids cold-start latency, fits in 4GB VRAM
- **`result.plot()` parameters** over custom drawing: minimal code, leverages built-in YOLO functionality
