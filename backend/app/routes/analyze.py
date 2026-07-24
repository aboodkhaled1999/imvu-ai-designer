from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.image_processor import ImageProcessor


router = APIRouter(
    prefix="/analyze",
    tags=["AI Analysis"],
)


# ================================
# Full AI Image Analysis
# ================================

@router.post("/clothing")
async def analyze_clothing(
    filename: str,
):
    """
    Run the complete AI clothing pipeline.

    Pipeline:
    1. Load uploaded image
    2. Remove background
    3. Detect dominant colors
    4. Generate texture
    """

    # Build input image path
    input_path = (
        Path(settings.UPLOAD_DIR)
        / filename
    )

    # Check if image exists
    if not input_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Uploaded image not found.",
        )

    try:
        processor = ImageProcessor()

        result = processor.process(
            image_path=str(input_path),
            remove_background=True,
            detect_colors=True,
            generate_texture=True,
        )

        return {
            "success": True,
            "message": (
                "Clothing image analyzed successfully."
            ),
            "result": result,
        }

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=404,
            detail=str(error),
        ) from error

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Clothing analysis failed."
            ),
        ) from error
