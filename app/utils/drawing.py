import cv2
import numpy as np
from PIL import Image

from app.models.schemas import Actor, ActorDistance


# COCO skeleton connections (pairs of keypoint indices)
COCO_SKELETON = [
    (0, 1), (0, 2), (1, 3), (2, 4),        # head
    (5, 6),                                   # shoulders
    (5, 7), (7, 9),                           # left arm
    (6, 8), (8, 10),                          # right arm
    (5, 11), (6, 12),                         # torso
    (11, 12),                                 # hips
    (11, 13), (13, 15),                       # left leg
    (12, 14), (14, 16),                       # right leg
]

SKELETON_COLOR = (0, 255, 0)   # green
KEYPOINT_COLOR = (0, 0, 255)   # red (BGR)
BBOX_COLOR = (255, 0, 0)       # blue (BGR)


def draw_pose_on_image(
    image: Image.Image,
    actors: list[Actor],
    scale_x: float = 1.0,
    scale_y: float = 1.0,
) -> Image.Image:
    """Draw bounding boxes, keypoints, and skeleton on image.

    Args:
        image: Original image to draw on (not modified in place).
        actors: Detected actors with keypoints.
        scale_x: X scale factor from inference size to original size.
        scale_y: Y scale factor from inference size to original size.
    """
    if not actors:
        return image

    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    for actor in actors:
        # Draw bounding box
        x1 = int(actor.bbox[0] * scale_x)
        y1 = int(actor.bbox[1] * scale_y)
        x2 = int(actor.bbox[2] * scale_x)
        y2 = int(actor.bbox[3] * scale_y)
        cv2.rectangle(img_bgr, (x1, y1), (x2, y2), BBOX_COLOR, 1, cv2.LINE_AA)

        # Collect scaled keypoint positions
        kp_coords = []
        for kp in actor.keypoints:
            kp_coords.append((int(kp.x * scale_x), int(kp.y * scale_y), kp.confidence))

        # Draw skeleton connections
        for i, j in COCO_SKELETON:
            if i < len(kp_coords) and j < len(kp_coords):
                if kp_coords[i][2] > 0.3 and kp_coords[j][2] > 0.3:
                    pt1 = (kp_coords[i][0], kp_coords[i][1])
                    pt2 = (kp_coords[j][0], kp_coords[j][1])
                    cv2.line(img_bgr, pt1, pt2, SKELETON_COLOR, 1, cv2.LINE_AA)

        # Draw keypoint dots
        for x, y, conf in kp_coords:
            if conf > 0.3:
                cv2.circle(img_bgr, (x, y), 3, KEYPOINT_COLOR, -1, cv2.LINE_AA)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)


def draw_distance_lines(
    image: Image.Image,
    distances: list[ActorDistance],
) -> Image.Image:
    if not distances:
        return image

    img_array = np.array(image)
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

    for dist in distances:
        pt_a = (int(dist.keypoint_a.x), int(dist.keypoint_a.y))
        pt_b = (int(dist.keypoint_b.x), int(dist.keypoint_b.y))

        cv2.line(img_bgr, pt_a, pt_b, (0, 255, 255), 1, cv2.LINE_AA)

        mid_x = (pt_a[0] + pt_b[0]) // 2
        mid_y = (pt_a[1] + pt_b[1]) // 2
        label = f"{dist.distance:.1f}"
        cv2.putText(
            img_bgr, label, (mid_x + 5, mid_y - 5),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1, cv2.LINE_AA,
        )

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img_rgb)
