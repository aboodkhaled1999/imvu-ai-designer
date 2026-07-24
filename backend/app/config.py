from pathlib import Path
from pydantic_settings import BaseSettings


# ================================
# Project Root
# ================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ================================
# Application Settings
# ================================

class Settings(BaseSettings):

    APP_NAME: str = "AI Clothing to IMVU Creator"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    API_PREFIX: str = "/api"

    # File Storage
    UPLOAD_DIR: str = "uploads"
    EXPORT_DIR: str = "exports"
    TEXTURE_DIR: str = "textures"

    # Maximum upload size
    MAX_UPLOAD_SIZE_MB: int = 20

    # Supported image formats
    ALLOWED_IMAGE_EXTENSIONS: tuple = (
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# ================================
# Global Settings Instance
# ================================

settings = Settings()
