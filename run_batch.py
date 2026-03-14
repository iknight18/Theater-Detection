# run_batch.py
import argparse
import gc
import json
import sys
import time
from pathlib import Path

import torch
from PIL import Image

from app.config import get_settings
from app.models.schemas import PoseMetadata
from app.services.depth_estimator import DepthEstimator
from app.services.sahi_estimator import SahiPoseEstimator
from app.services.yolo_estimator import YoloPoseEstimator
from app.services.base import PoseResult
from app.utils.distance import compute_actor_distances
from app.utils.drawing import draw_distance_lines, draw_pose_on_image
from app.utils.image import resize_if_needed, adaptive_enhance

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

AVAILABLE_MODELS = {
    "yolov8": "yolov8m-pose.pt",
    "yolov11": "yolo11m-pose.pt",
}


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
        "--confidence", type=float, default=0.25,
        help="Minimum detection confidence (default: 0.25)"
    )
    parser.add_argument(
        "--models", type=str, default="yolov8",
        help=f"Comma-separated model names to compare (default: yolov8). "
             f"Available: {', '.join(AVAILABLE_MODELS.keys())}"
    )
    return parser.parse_args(argv)


def collect_images(input_dir: Path) -> list[Path]:
    return sorted(
        p for p in input_dir.iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def _save_strategy_results(
    strategy_dir: Path,
    original_image: Image.Image,
    result: PoseResult,
    depth_estimator: DepthEstimator,
    inference_image: Image.Image,
    source_file: str,
    estimator_name: str,
    original_width: int,
    original_height: int,
    scale_x: float,
    scale_y: float,
) -> None:
    """Save annotated image and metadata for one strategy."""
    strategy_dir.mkdir(parents=True, exist_ok=True)

    # Save the exact image fed to the model
    inference_image.save(strategy_dir / "input.png", format="PNG")

    # Draw detections on the original image
    annotated = draw_pose_on_image(
        original_image, result.actors, scale_x=scale_x, scale_y=scale_y
    )

    # Compute distances if multiple actors
    distances = []
    if len(result.actors) >= 2:
        depth_map = depth_estimator.estimate(inference_image)
        distances = compute_actor_distances(result.actors, depth_map)
        if distances:
            annotated = draw_distance_lines(annotated, distances)

    annotated.save(strategy_dir / "annotated.png", format="PNG")

    metadata = {
        "source_file": source_file,
        "actors": [a.model_dump() for a in result.actors],
        "distances": [d.model_dump() for d in distances],
        "metadata": PoseMetadata(
            image_width=original_width,
            image_height=original_height,
            model=estimator_name,
            inference_time_ms=round(result.inference_time_ms, 2),
            actor_count=len(result.actors),
        ).model_dump(),
    }
    with open(strategy_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)


def process_image_all_strategies(
    image_path: Path,
    output_dir: Path,
    estimator: YoloPoseEstimator,
    sahi_estimator: SahiPoseEstimator,
    depth_estimator: DepthEstimator,
    confidence: float,
    max_image_size: int,
    model_label: str,
) -> dict[str, int]:
    """Run all 3 strategies on one image for a given model. Returns actor counts per strategy."""
    img = Image.open(image_path).convert("RGB")
    original_width, original_height = img.size
    resized = resize_if_needed(img, max_size=max_image_size)

    scale_x = 1.0
    scale_y = 1.0

    enhanced = adaptive_enhance(resized)

    # Output subfolder: results/<image_name>/<model_label>/
    subfolder = output_dir / image_path.name
    model_dir = subfolder / model_label
    model_dir.mkdir(parents=True, exist_ok=True)

    # Export intermediate images (once per image, not per model)
    original_path = subfolder / "original.png"
    if not original_path.exists():
        resized.save(original_path, format="PNG")
    enhanced_path = subfolder / "enhanced.png"
    if not enhanced_path.exists():
        enhanced.save(enhanced_path, format="PNG")

    counts = {}

    # Strategy 1: Baseline
    result_baseline = estimator.predict(resized, confidence_threshold=confidence)
    _save_strategy_results(
        model_dir / "baseline", resized, result_baseline,
        depth_estimator, resized, image_path.name, estimator.model_name,
        original_width, original_height, scale_x, scale_y,
    )
    counts["baseline"] = len(result_baseline.actors)

    # Strategy 2: Adaptive Enhancement + YOLO
    result_enhanced = estimator.predict(enhanced, confidence_threshold=confidence)
    _save_strategy_results(
        model_dir / "enhanced", resized, result_enhanced,
        depth_estimator, enhanced, image_path.name, estimator.model_name,
        original_width, original_height, scale_x, scale_y,
    )
    counts["enhanced"] = len(result_enhanced.actors)

    # Strategy 3: Adaptive Enhancement + SAHI
    result_sahi = sahi_estimator.predict(enhanced, confidence_threshold=confidence)
    _save_strategy_results(
        model_dir / "sahi", resized, result_sahi,
        depth_estimator, enhanced, image_path.name, estimator.model_name,
        original_width, original_height, scale_x, scale_y,
    )
    counts["sahi"] = len(result_sahi.actors)

    # Comparison JSON per model
    comparison = {}
    for name, result in [
        ("baseline", result_baseline),
        ("enhanced", result_enhanced),
        ("sahi", result_sahi),
    ]:
        comparison[name] = {
            "actor_count": len(result.actors),
            "inference_time_ms": round(result.inference_time_ms, 2),
            "avg_confidence": round(
                sum(a.confidence for a in result.actors) / len(result.actors), 3
            ) if result.actors else 0.0,
        }
    with open(model_dir / "comparison.json", "w") as f:
        json.dump(comparison, f, indent=2)

    return counts


def _unload_models(*estimators) -> None:
    """Unload models and free VRAM."""
    for est in estimators:
        if hasattr(est, '_model') and est._model is not None:
            del est._model
            est._model = None
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    if not args.input.is_dir():
        print(f"Error: '{args.input}' is not a directory", file=sys.stderr)
        sys.exit(1)

    images = collect_images(args.input)
    if not images:
        print(f"No images found in '{args.input}'", file=sys.stderr)
        sys.exit(1)

    model_names = [m.strip() for m in args.models.split(",")]
    for name in model_names:
        if name not in AVAILABLE_MODELS:
            print(f"Error: Unknown model '{name}'. Available: {', '.join(AVAILABLE_MODELS.keys())}", file=sys.stderr)
            sys.exit(1)

    print(f"Found {len(images)} images in '{args.input}'")
    print(f"Models to compare: {', '.join(model_names)}")

    settings = get_settings()

    # Load depth estimator once (shared across all models)
    print("Loading depth estimator...")
    depth_estimator = DepthEstimator(device=settings.device)
    depth_estimator.load_model()

    args.output.mkdir(parents=True, exist_ok=True)
    start_time = time.perf_counter()

    # Run each model sequentially to fit in VRAM
    all_totals = {}
    for model_label in model_names:
        model_file = AVAILABLE_MODELS[model_label]
        print(f"\n{'='*60}")
        print(f"Loading {model_label} ({model_file})...")

        estimator = YoloPoseEstimator(model_name=model_file, device=settings.device)
        estimator.load_model()

        sahi_estimator = SahiPoseEstimator(model_path=model_file, device=settings.device)
        sahi_estimator.load_model()

        print(f"Processing images with {model_label}...\n")

        total_counts = {"baseline": 0, "enhanced": 0, "sahi": 0}

        for i, image_path in enumerate(images, 1):
            print(f"  [{i}/{len(images)}] {image_path.name}...", end=" ")
            try:
                counts = process_image_all_strategies(
                    image_path, args.output, estimator, sahi_estimator,
                    depth_estimator, args.confidence, settings.max_image_size,
                    model_label,
                )
                for k, v in counts.items():
                    total_counts[k] += v
                print(f"baseline={counts['baseline']} enhanced={counts['enhanced']} sahi={counts['sahi']}")
            except Exception as e:
                print(f"FAILED ({type(e).__name__}): {e}")

        all_totals[model_label] = total_counts

        # Unload model before loading next one
        print(f"\n{model_label} totals — baseline: {total_counts['baseline']}, "
              f"enhanced: {total_counts['enhanced']}, sahi: {total_counts['sahi']}")
        _unload_models(estimator, sahi_estimator)

    elapsed = time.perf_counter() - start_time
    print(f"\n{'='*60}")
    print(f"Done! {len(images)} images, {len(model_names)} models, {elapsed:.1f}s")
    for model_label, counts in all_totals.items():
        print(f"  {model_label}: baseline={counts['baseline']} enhanced={counts['enhanced']} sahi={counts['sahi']}")


if __name__ == "__main__":
    main()
