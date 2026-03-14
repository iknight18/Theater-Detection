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
