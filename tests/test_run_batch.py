# tests/test_run_batch.py
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

from PIL import Image

from app.services.base import PoseResult
from run_batch import collect_images, process_image_all_strategies

SCRIPT_PATH = str(Path(__file__).resolve().parent.parent / "run_batch.py")

def test_batch_help_flag():
    """Script should accept --help without error."""
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH, "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "images" in result.stdout.lower()

def test_batch_missing_input_dir():
    """Script should fail with clear error when input dir is missing."""
    result = subprocess.run(
        [sys.executable, SCRIPT_PATH, "nonexistent_folder_xyz"],
        capture_output=True, text=True
    )
    assert result.returncode != 0


# --- collect_images tests ---

def test_collect_images_filters_extensions(tmp_path):
    """Only .jpg, .jpeg, .png, .webp files should be collected."""
    (tmp_path / "a.jpg").touch()
    (tmp_path / "b.png").touch()
    (tmp_path / "c.txt").touch()
    (tmp_path / "d.webp").touch()
    (tmp_path / "e.bmp").touch()

    result = collect_images(tmp_path)
    names = [p.name for p in result]
    assert names == ["a.jpg", "b.png", "d.webp"]

def test_collect_images_empty_dir(tmp_path):
    """Empty directory should return empty list."""
    assert collect_images(tmp_path) == []

def test_collect_images_sorted(tmp_path):
    """Results should be sorted alphabetically."""
    (tmp_path / "z.jpg").touch()
    (tmp_path / "a.jpg").touch()
    (tmp_path / "m.png").touch()

    result = collect_images(tmp_path)
    names = [p.name for p in result]
    assert names == ["a.jpg", "m.png", "z.jpg"]


# --- process_image_all_strategies tests ---

def test_process_image_all_strategies_creates_structure(tmp_path):
    """All 3 strategy folders should be created with annotated + metadata."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    img = Image.new("RGB", (640, 480), "white")
    img_path = input_dir / "test_photo.png"
    img.save(img_path)

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    mock_estimator = MagicMock()
    mock_estimator.model_name = "yolov8m-pose"
    mock_estimator.predict.return_value = PoseResult(
        actors=[],
        annotated_image=Image.new("RGB", (640, 480), "gray"),
        inference_time_ms=10.0,
    )

    mock_sahi = MagicMock()
    mock_sahi.predict.return_value = PoseResult(
        actors=[],
        inference_time_ms=15.0,
    )

    mock_depth = MagicMock()

    process_image_all_strategies(
        img_path, output_dir, mock_estimator, mock_sahi, mock_depth, 0.5, 1920,
    )

    subfolder = output_dir / "test_photo.png"
    assert subfolder.is_dir()

    # Original and enhanced images exported
    assert (subfolder / "original.png").is_file()
    assert (subfolder / "enhanced.png").is_file()

    # All 3 strategy folders
    for strategy in ["baseline", "enhanced", "sahi"]:
        strategy_dir = subfolder / strategy
        assert strategy_dir.is_dir(), f"Missing {strategy}/ folder"
        assert (strategy_dir / "annotated.png").is_file(), f"Missing {strategy}/annotated.png"
        assert (strategy_dir / "metadata.json").is_file(), f"Missing {strategy}/metadata.json"

    # Comparison JSON
    assert (subfolder / "comparison.json").is_file()


def test_process_image_comparison_json_structure(tmp_path):
    """comparison.json should contain counts for all strategies."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    img = Image.new("RGB", (640, 480), "white")
    img_path = input_dir / "test_photo.png"
    img.save(img_path)

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    mock_estimator = MagicMock()
    mock_estimator.model_name = "yolov8m-pose"
    mock_estimator.predict.return_value = PoseResult(
        actors=[],
        annotated_image=Image.new("RGB", (640, 480), "gray"),
        inference_time_ms=10.0,
    )

    mock_sahi = MagicMock()
    mock_sahi.predict.return_value = PoseResult(actors=[], inference_time_ms=15.0)

    mock_depth = MagicMock()

    process_image_all_strategies(
        img_path, output_dir, mock_estimator, mock_sahi, mock_depth, 0.5, 1920,
    )

    subfolder = output_dir / "test_photo.png"
    with open(subfolder / "comparison.json") as f:
        data = json.load(f)

    assert "baseline" in data
    assert "enhanced" in data
    assert "sahi" in data
    for strategy in ["baseline", "enhanced", "sahi"]:
        assert "actor_count" in data[strategy]
        assert "inference_time_ms" in data[strategy]
        assert "avg_confidence" in data[strategy]
