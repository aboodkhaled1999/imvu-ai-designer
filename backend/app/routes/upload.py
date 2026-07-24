from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.services.file_validator import FileValidator
from app.utils import (
    ensure_directories,
    generate_unique_filename,
)


router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


# ================================
# Upload Clothing Image
# ================================

@router.post("/clothing")
async def upload_clothing_image(
    file: UploadFile = File(...),
):
    """
    Upload and validate a clothing image.

    Process:
    1. Validate filename
    2. Validate extension
    3. Check file size
    4. Save image
    5. Validate actual image content
    """

    # Create required directories
    ensure_directories()

    # ================================
    # Basic Filename Validation
    # ================================

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided.",
        )

    # ================================
    # Extension Validation
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
    # Read File
    # ================================

    file_data = await file.read()

    # ================================
    # File Size Validation
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
    # Generate Secure Filename
    # ================================

    filename = (
        generate_unique_filename(
            file.filename
        )
    )

    # ================================
    # Build Upload Path
    # ================================

    upload_path = (
        Path(settings.UPLOAD_DIR)
        / filename
    )

    # ================================
    # Save File
    # ================================

    try:

        with open(
            upload_path,
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
            str(upload_path)
        )
    )

    if not validation["valid"]:

        # Delete invalid file
        if upload_path.exists():
            upload_path.unlink()

        raise HTTPException(
            status_code=400,
            detail=(
                "The uploaded file is not "
                "a valid image."
            ),
        )

    # ================================
    # Return Response
    # ================================

    return {
        "success": True,
        "message": (
            "Clothing image uploaded "
            "and validated successfully."
        ),
        "filename": filename,
        "path": str(
            upload_path
        ),
        "size_bytes": len(
            file_data
        ),
        "validation": validation,
    }
