# tests/test_run_batch.py
import subprocess
import sys

def test_batch_help_flag():
    """Script should accept --help without error."""
    result = subprocess.run(
        [sys.executable, "run_batch.py", "--help"],
        capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "images" in result.stdout.lower()

def test_batch_missing_input_dir():
    """Script should fail with clear error when input dir is missing."""
    result = subprocess.run(
        [sys.executable, "run_batch.py", "nonexistent_folder_xyz"],
        capture_output=True, text=True
    )
    assert result.returncode != 0
