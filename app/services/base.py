from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from PIL import Image

from app.models.schemas import Actor


@dataclass
class PoseResult:
    actors: list[Actor] = field(default_factory=list)
    annotated_image: Image.Image | None = None
    inference_time_ms: float = 0.0


class PoseEstimator(ABC):
    @abstractmethod
    def load_model(self) -> None:
        """Load the model into memory."""
        ...

    @abstractmethod
    def predict(self, image: Image.Image, confidence_threshold: float = 0.5) -> PoseResult:
        """Run pose estimation on an image and return results."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier string."""
        ...
