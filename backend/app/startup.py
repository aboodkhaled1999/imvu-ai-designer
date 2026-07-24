from pathlib import Path

from app.config import settings


def initialize_project_directories():
    """
    Create all required project directories
    when the application starts.
    """

    directories = [
        settings.UPLOAD_DIR,
        settings.EXPORT_DIR,
        settings.TEXTURE_DIR,
        Path(settings.UPLOAD_DIR) / "processed",
    ]

    for directory in directories:
        Path(directory).mkdir(
            parents=True,
            exist_ok=True,
        )

    return {
        "success": True,
        "directories": [
            str(directory)
            for directory in directories
        ],
    }
