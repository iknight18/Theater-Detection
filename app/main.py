from contextlib import asynccontextmanager

from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.config import get_settings
from app.services.yolo_estimator import YoloPoseEstimator

estimator: YoloPoseEstimator | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global estimator
    settings = get_settings()
    estimator = YoloPoseEstimator(
        model_name=settings.model_name,
        device=settings.device,
    )
    estimator.load_model()
    yield
    estimator = None


app = FastAPI(
    title="Theater Pose Estimation API",
    description="Pose estimation for theater performance analysis. Upload an image to detect actor poses.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Theater Pose Estimation API", "docs": "/scalar"}


@app.get("/scalar", include_in_schema=False)
async def scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Theater Pose Estimation API",
    )


def get_estimator() -> YoloPoseEstimator:
    if estimator is None:
        raise RuntimeError("Model not initialized")
    return estimator
