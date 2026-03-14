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
