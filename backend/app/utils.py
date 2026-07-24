from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.config import settings


# ================================
# Directory Management
# ================================

def ensure_directories():
    """
    Create all required project directories
    if they do not already exist.
    """

    directories = [
        settings.UPLOAD_DIR,
        settings.EXPORT_DIR,
        settings.TEXTURE_DIR,
    ]

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )


# ================================
# File Validation
# ================================

def validate_image_extension(filename: str) -> bool:
    """
    Check if the uploaded file has
    a supported image extension.
    """

    if not filename:
        return False

    extension = Path(filename).suffix.lower()

    return extension in settings.ALLOWED_IMAGE_EXTENSIONS


# ================================
# Generate Unique Filename
# ================================

def generate_unique_filename(
    original_filename: str,
) -> str:
    """
    Generate a unique filename while
    preserving the original file extension.
    """

    extension = Path(original_filename).suffix.lower()

    unique_id = uuid4().hex

    return f"{unique_id}{extension}"


# ================================
# Upload File Validation
# ================================

async def validate_upload_file(
    file: UploadFile,
) -> bool:
    """
    Validate an uploaded file.

    Checks:
    - Filename exists
    - File extension is supported
    """

    if not file.filename:
        return False

    if not validate_image_extension(
        file.filename
    ):
        return False

    return True
