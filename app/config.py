from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_name: str = "yolov8m-pose.pt"
    device: str = "auto"  # "auto", "cpu", "cuda", "cuda:0"
    confidence_threshold: float = 0.5
    max_image_size: int = 1920  # max dimension in px, images resized if larger
    max_file_size_mb: int = 10
    allowed_extensions: set[str] = {"jpg", "jpeg", "png", "webp"}
    min_image_dimension: int = 64  # minimum width/height in px

    model_config = {"env_prefix": "", "case_sensitive": False}


def get_settings() -> Settings:
    return Settings()
