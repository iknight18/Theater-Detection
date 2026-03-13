import base64
import io

from PIL import Image


def validate_image(
    data: bytes,
    allowed_extensions: set[str],
    max_file_size_mb: int,
    min_dimension: int,
) -> Image.Image:
    max_bytes = max_file_size_mb * 1024 * 1024
    if len(data) > max_bytes:
        raise ValueError(f"File size {len(data)} exceeds maximum {max_bytes} bytes")

    try:
        img = Image.open(io.BytesIO(data))
        img.load()
    except Exception:
        raise ValueError("Could not open image — unsupported or corrupt file")

    fmt = (img.format or "").lower()
    if fmt == "jpeg":
        fmt = "jpg"
    if fmt not in allowed_extensions and "jpg" not in allowed_extensions:
        format_map = {"jpeg": "jpg", "jpg": "jpg", "png": "png", "webp": "webp"}
        mapped = format_map.get(fmt, fmt)
        if mapped not in allowed_extensions:
            raise ValueError(f"Image format '{fmt}' not allowed. Allowed: {allowed_extensions}")

    w, h = img.size
    if w < min_dimension or h < min_dimension:
        raise ValueError(f"Image too small ({w}x{h}). Minimum dimension: {min_dimension}px")

    if img.mode != "RGB":
        img = img.convert("RGB")

    return img


def resize_if_needed(img: Image.Image, max_size: int) -> Image.Image:
    w, h = img.size
    if max(w, h) <= max_size:
        return img

    if w >= h:
        new_w = max_size
        new_h = int(h * (max_size / w))
    else:
        new_h = max_size
        new_w = int(w * (max_size / h))

    return img.resize((new_w, new_h), Image.LANCZOS)


def image_to_base64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")
