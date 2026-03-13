from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from scalar_fastapi import get_scalar_api_reference

from app.config import get_settings
from app.services.yolo_estimator import YoloPoseEstimator

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    estimator = YoloPoseEstimator(
        model_name=settings.model_name,
        device=settings.device,
    )
    estimator.load_model()
    app.state.estimator = estimator
    yield
    app.state.estimator = None


app = FastAPI(
    title="Theater Pose Estimation API",
    description="Pose estimation for theater performance analysis. Upload an image to detect actor poses.",
    version="0.1.0",
    lifespan=lifespan,
)


from app.api.routes.pose import router as pose_router
from app.utils.image import ANNOTATED_DIR

app.include_router(pose_router)
app.mount("/annotated_images", StaticFiles(directory=str(ANNOTATED_DIR)), name="annotated_images")


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
    estimator = getattr(app.state, "estimator", None)
    if estimator is None:
        raise RuntimeError("Model not initialized")
    return estimator
