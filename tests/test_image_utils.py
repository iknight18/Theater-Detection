import io
import numpy as np
import pytest
from PIL import Image
from app.utils.image import validate_image, resize_if_needed, image_to_base64
from app.utils.image import adaptive_enhance


def _make_test_image(width: int, height: int, fmt: str = "PNG") -> bytes:
    img = Image.new("RGB", (width, height), color="red")
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def test_validate_image_valid():
    data = _make_test_image(640, 480, "PNG")
    img = validate_image(data, allowed_extensions={"png", "jpg"}, max_file_size_mb=10, min_dimension=64)
    assert img.size == (640, 480)


def test_validate_image_too_large():
    data = b"x" * (11 * 1024 * 1024)  # 11MB
    with pytest.raises(ValueError, match="File size"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_validate_image_too_small():
    data = _make_test_image(32, 32, "PNG")
    with pytest.raises(ValueError, match="too small"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_validate_image_invalid_format():
    data = b"not an image"
    with pytest.raises(ValueError, match="Could not open"):
        validate_image(data, allowed_extensions={"png"}, max_file_size_mb=10, min_dimension=64)


def test_resize_if_needed_no_resize():
    img = Image.new("RGB", (800, 600))
    result = resize_if_needed(img, max_size=1920)
    assert result.size == (800, 600)


def test_resize_if_needed_downscale():
    img = Image.new("RGB", (3840, 2160))
    result = resize_if_needed(img, max_size=1920)
    assert max(result.size) == 1920
    # Aspect ratio preserved
    assert result.size == (1920, 1080)


def test_image_to_base64():
    img = Image.new("RGB", (100, 100), color="blue")
    b64 = image_to_base64(img)
    assert isinstance(b64, str)
    assert len(b64) > 0


def test_adaptive_enhance_returns_image():
    """adaptive_enhance should return a PIL Image."""
    img = Image.new("RGB", (640, 480), color="gray")
    result = adaptive_enhance(img)
    assert isinstance(result, Image.Image)
    assert result.size == (640, 480)
    assert result.mode == "RGB"


def test_adaptive_enhance_dark_image_brightens():
    """A very dark image should be brightened significantly."""
    # Create a dark image (mean luminance ~25)
    img = Image.new("RGB", (200, 200), color=(25, 25, 25))
    result = adaptive_enhance(img)
    result_arr = np.array(result)
    input_arr = np.array(img)
    # Enhanced image should have higher mean brightness
    assert result_arr.mean() > input_arr.mean()


def test_adaptive_enhance_bright_image_minimal_change():
    """A well-lit image should not be over-brightened."""
    img = Image.new("RGB", (200, 200), color=(200, 200, 200))
    result = adaptive_enhance(img)
    result_arr = np.array(result)
    input_arr = np.array(img)
    # Should not change dramatically (within 30% of original mean)
    assert abs(result_arr.mean() - input_arr.mean()) / input_arr.mean() < 0.3


def test_adaptive_enhance_colored_lighting():
    """Colored stage lighting should not break enhancement."""
    # Simulate warm tungsten (reddish tint)
    img = Image.new("RGB", (200, 200), color=(180, 100, 50))
    result = adaptive_enhance(img)
    assert isinstance(result, Image.Image)
    assert result.size == (200, 200)
