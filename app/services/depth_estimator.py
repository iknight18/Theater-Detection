import numpy as np
import torch
from PIL import Image
from transformers import pipeline


class DepthEstimator:
    def __init__(self, device: str = "auto"):
        self._device = device
        self._pipe = None

    def load_model(self) -> None:
        device_arg = self._resolve_device()
        self._pipe = pipeline(
            task="depth-estimation",
            model="depth-anything/Depth-Anything-V2-Small-hf",
            device=device_arg,
        )

    def _resolve_device(self) -> str:
        if self._device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return self._device

    def estimate(self, image: Image.Image) -> np.ndarray:
        if self._pipe is None:
            raise RuntimeError("Depth model not loaded. Call load_model() first.")

        original_size = image.size  # (width, height)

        result = self._pipe(image)
        depth_map = np.array(result["depth"], dtype=np.float32)

        # Resize back to input dimensions if pipeline returned a different size
        h, w = original_size[1], original_size[0]
        if depth_map.shape != (h, w):
            depth_pil = Image.fromarray(depth_map)
            depth_pil = depth_pil.resize(original_size, Image.BILINEAR)
            depth_map = np.array(depth_pil, dtype=np.float32)

        # Normalize to 0-1 range
        d_min, d_max = depth_map.min(), depth_map.max()
        if d_max - d_min > 0:
            depth_map = (depth_map - d_min) / (d_max - d_min)
        else:
            depth_map = np.zeros_like(depth_map)

        return depth_map
