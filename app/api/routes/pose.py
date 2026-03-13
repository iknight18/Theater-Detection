import uuid

from fastapi import APIRouter, File, Query, Request, UploadFile, HTTPException

from app.config import get_settings
from app.models.schemas import PoseEstimationResponse, PoseMetadata
from app.utils.image import validate_image, resize_if_needed, image_to_base64

router = APIRouter(prefix="/api/v1/pose", tags=["Pose Estimation"])


@router.post("/estimate", response_model=PoseEstimationResponse)
async def estimate_pose(
    request: Request,
    file: UploadFile = File(..., description="Image file (JPEG, PNG, or WebP)"),
    confidence_threshold: float = Query(
        default=0.5, ge=0.0, le=1.0, description="Minimum detection confidence"
    ),
    return_image: bool = Query(
        default=True, description="Include annotated image in response"
    ),
):
    settings = get_settings()

    data = await file.read()

    try:
        image = validate_image(
            data,
            allowed_extensions=settings.allowed_extensions,
            max_file_size_mb=settings.max_file_size_mb,
            min_dimension=settings.min_image_dimension,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    original_width, original_height = image.size
    image = resize_if_needed(image, max_size=settings.max_image_size)

    estimator = request.app.state.estimator
    if estimator is None:
        raise HTTPException(status_code=503, detail="Model not initialized")

    result = estimator.predict(image, confidence_threshold=confidence_threshold)

    annotated_b64 = None
    if return_image and result.annotated_image is not None:
        annotated_b64 = image_to_base64(result.annotated_image)

    return PoseEstimationResponse(
        image_id=str(uuid.uuid4()),
        actors=result.actors,
        annotated_image=annotated_b64,
        metadata=PoseMetadata(
            image_width=original_width,
            image_height=original_height,
            model=estimator.model_name,
            inference_time_ms=round(result.inference_time_ms, 2),
            actor_count=len(result.actors),
        ),
    )
