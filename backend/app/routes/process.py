from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.config import settings
from app.services.background_remover import (
    BackgroundRemover,
)


router = APIRouter(
    prefix="/process",
    tags=["Processing"],
)


# ================================
# Remove Background
# ================================

@router.post("/remove-background")
async def remove_background(
    filename: str,
):
    """
    Remove the background from an
    uploaded clothing image.
    """

    # Build input image path
    input_path = (
        Path(settings.UPLOAD_DIR)
        / filename
    )

    # Check if file exists
    if not input_path.exists():
        raise HTTPException(
            status_code=404,
            detail=(
                "Uploaded image not found."
            ),
        )

    try:

        remover = BackgroundRemover(
            output_dir=(
                f"{settings.UPLOAD_DIR}"
                "/processed"
            )
        )

        result = (
            remover.process(
                str(input_path)
            )
        )

        return {
            "success": True,
            "message": (
                "Background removed successfully."
            ),
            "input_file": filename,
            "output_file": result[
                "output_path"
            ],
            "transparent": True,
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Background removal failed."
            ),
        ) from error
