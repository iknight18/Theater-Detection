from app.config import Settings


def test_default_settings():
    settings = Settings()
    assert settings.model_name == "yolov8m-pose.pt"
    assert settings.device == "auto"
    assert settings.confidence_threshold == 0.5
    assert settings.max_image_size == 1920
    assert settings.max_file_size_mb == 10
    assert settings.allowed_extensions == {"jpg", "jpeg", "png", "webp"}
    assert settings.min_image_dimension == 64


def test_custom_settings_from_env(monkeypatch):
    monkeypatch.setenv("MODEL_NAME", "yolov8n-pose.pt")
    monkeypatch.setenv("CONFIDENCE_THRESHOLD", "0.7")
    settings = Settings()
    assert settings.model_name == "yolov8n-pose.pt"
    assert settings.confidence_threshold == 0.7
