# tests/test_run_batch.py
import subprocess
import sys
from pathlib import Path

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
