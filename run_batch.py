# run_batch.py
import argparse
import json
import sys
import time
from pathlib import Path

from PIL import Image

from app.config import get_settings
from app.models.schemas import PoseMetadata
from app.services.depth_estimator import DepthEstimator
from app.services.yolo_estimator import YoloPoseEstimator
from app.utils.distance import compute_actor_distances
from app.utils.drawing import draw_distance_lines
from app.utils.image import resize_if_needed

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run pose estimation on a folder of images"
    )
    parser.add_argument(
        "input", type=Path, help="Path to folder containing images"
    )
    parser.add_argument(
        "--output", type=Path, default=Path("results"),
        help="Output folder (default: results/)"
    )
    parser.add_argument(
        "--confidence", type=float, default=0.5,
        help="Minimum detection confidence (default: 0.5)"
    )
    return parser.parse_args(argv)


def collect_images(input_dir: Path) -> list[Path]:
    return sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def process_image(
    image_path: Path,
    output_dir: Path,
    estimator: YoloPoseEstimator,
    depth_estimator: DepthEstimator,
    confidence: float,
    max_image_size: int,
) -> int:
    """Process a single image. Returns actor count."""
    img = Image.open(image_path).convert("RGB")
    original_width, original_height = img.size
    img = resize_if_needed(img, max_size=max_image_size)

    result = estimator.predict(img, confidence_threshold=confidence)

    distances = []
    if len(result.actors) >= 2:
        depth_map = depth_estimator.estimate(img)
        distances = compute_actor_distances(result.actors, depth_map)
        if result.annotated_image is not None and distances:
            result.annotated_image = draw_distance_lines(
                result.annotated_image, distances
            )

    # Create output subfolder named after image (minus extension)
    subfolder = output_dir / image_path.name
    subfolder.mkdir(parents=True, exist_ok=True)

    # Save annotated image
    if result.annotated_image is not None:
        result.annotated_image.save(subfolder / "annotated.png", format="PNG")

    # Save metadata JSON
    metadata = {
        "source_file": image_path.name,
        "actors": [a.model_dump() for a in result.actors],
        "distances": [d.model_dump() for d in distances],
        "metadata": PoseMetadata(
            image_width=original_width,
            image_height=original_height,
            model=estimator.model_name,
            inference_time_ms=round(result.inference_time_ms, 2),
            actor_count=len(result.actors),
        ).model_dump(),
    }
    with open(subfolder / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return len(result.actors)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if not args.input.is_dir():
        print(f"Error: '{args.input}' is not a directory", file=sys.stderr)
        sys.exit(1)

    images = collect_images(args.input)
    if not images:
        print(f"No images found in '{args.input}'", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(images)} images in '{args.input}'")
    print("Loading models...")

    settings = get_settings()

    estimator = YoloPoseEstimator(
        model_name=settings.model_name, device=settings.device
    )
    estimator.load_model()

    depth_estimator = DepthEstimator(device=settings.device)
    depth_estimator.load_model()

    print("Models loaded. Processing images...\n")

    args.output.mkdir(parents=True, exist_ok=True)

    total_actors = 0
    start_time = time.perf_counter()

    for i, image_path in enumerate(images, 1):
        print(f"[{i}/{len(images)}] Processing {image_path.name}...", end=" ")
        try:
            actor_count = process_image(
                image_path, args.output, estimator, depth_estimator,
                args.confidence, settings.max_image_size,
            )
            total_actors += actor_count
            print(f"{actor_count} actors")
        except Exception as e:
            print(f"FAILED ({type(e).__name__}): {e}")

    elapsed = time.perf_counter() - start_time
    print(f"\nDone! {len(images)} images, {total_actors} actors, {elapsed:.1f}s")


if __name__ == "__main__":
    main()
