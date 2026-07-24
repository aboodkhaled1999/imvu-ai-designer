from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.services.file_validator import FileValidator
from app.services.image_processor import ImageProcessor
from app.utils import (
    ensure_directories,
    generate_unique_filename,
)


router = APIRouter(
    prefix="/pipeline",
    tags=["AI Pipeline"],
)


# ================================
# Complete AI Clothing Pipeline
# ================================

@router.post("/process")
async def process_clothing_pipeline(
    file: UploadFile = File(...),
):
    """
    Complete AI clothing processing pipeline.

    Steps:
    1. Validate uploaded file
    2. Save image
    3. Validate actual image
    4. Remove background
    5. Detect dominant colors
    6. Generate texture
    """

    # ================================
    # Initialize Directories
    # ================================

    ensure_directories()

    # ================================
    # Validate Filename
    # ================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    # ================================
    # Validate Extension
    # ================================

    if not FileValidator.validate_extension(
        file.filename
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported image format. "
                "Allowed formats: "
                "JPG, JPEG, PNG, WEBP."
            ),
        )

    # ================================
    # Read Uploaded File
    # ================================

    file_data = await file.read()

    # ================================
    # Validate File Size
    # ================================

    max_size = (
        settings.MAX_UPLOAD_SIZE_MB
        * 1024
        * 1024
    )

    if len(file_data) > max_size:
        raise HTTPException(
            status_code=413,
            detail=(
                f"File is too large. "
                f"Maximum allowed size is "
                f"{settings.MAX_UPLOAD_SIZE_MB} MB."
            ),
        )

    # ================================
    # Generate Unique Filename
    # ================================

    filename = (
        generate_unique_filename(
            file.filename
        )
    )

    input_path = (
        Path(settings.UPLOAD_DIR)
        / filename
    )

    # ================================
    # Save Uploaded File
    # ================================

    try:

        with open(
            input_path,
            "wb",
        ) as buffer:

            buffer.write(
                file_data
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save uploaded file."
            ),
        ) from error

    # ================================
    # Validate Actual Image
    # ================================

    validation = (
        FileValidator.validate(
            str(input_path)
        )
    )

    if not validation["valid"]:

        if input_path.exists():
            input_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file is not "
                "a valid image."
            ),
        )

    # ================================
    # Run AI Pipeline
    # ================================

    try:

        processor = ImageProcessor()

        result = processor.process(
            image_path=str(
                input_path
            ),
            remove_background=True,
            detect_colors=True,
            generate_texture=True,
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=(
                "AI image processing failed."
            ),
        ) from error

    # ================================
    # Return Complete Result
    # ================================

    return {
        "success": True,
        "message": (
            "Clothing image processed "
            "successfully."
        ),
        "input": {
            "filename": filename,
            "path": str(
                input_path
            ),
            "size_bytes": len(
                file_data
            ),
        },
        "validation": validation,
        "processing": result,
    }
