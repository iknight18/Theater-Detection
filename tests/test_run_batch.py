# tests/test_run_batch.py
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

from PIL import Image

from app.services.base import PoseResult
from run_batch import collect_images, process_image

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


# --- process_image tests ---

def test_process_image_creates_output(tmp_path):
    """process_image should create subfolder with annotated.png and metadata.json."""
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

    mock_depth = MagicMock()

    process_image(img_path, output_dir, mock_estimator, mock_depth, 0.5, 1920)

    # NOTE: subfolder uses image_path.name (full filename with extension)
    subfolder = output_dir / "test_photo.png"
    assert subfolder.is_dir()
    assert (subfolder / "annotated.png").is_file()
    assert (subfolder / "metadata.json").is_file()

    with open(subfolder / "metadata.json") as f:
        data = json.load(f)
    assert data["source_file"] == "test_photo.png"
    assert data["metadata"]["actor_count"] == 0
    assert data["metadata"]["model"] == "yolov8m-pose"
