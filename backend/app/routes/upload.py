from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.config import settings
from app.utils import (
    ensure_directories,
    generate_unique_filename,
    validate_upload_file,
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
    Upload a clothing image.

    The uploaded image is:
    1. Validated
    2. Given a unique filename
    3. Saved inside the upload directory
    """

    # Create required directories
    ensure_directories()

    # Validate uploaded file
    is_valid = await validate_upload_file(file)

    if not is_valid:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid image file. "
                "Supported formats: "
                f"{', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}"
            ),
        )

    # Generate unique filename
    filename = generate_unique_filename(
        file.filename
    )

    # Create upload path
    upload_path = (
        Path(settings.UPLOAD_DIR)
        / filename
    )

    # Read uploaded file
    file_data = await file.read()

    # Check file size
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

    # Save file
    try:
        with open(
            upload_path,
            "wb",
        ) as buffer:
            buffer.write(file_data)

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save uploaded file."
            ),
        ) from error

    # Return upload information
    return {
        "success": True,
        "message": (
            "Clothing image uploaded successfully."
        ),
        "filename": filename,
        "path": str(upload_path),
        "size_bytes": len(file_data),
    }
