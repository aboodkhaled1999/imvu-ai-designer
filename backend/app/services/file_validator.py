from pathlib import Path

from PIL import Image


class FileValidator:
    """
    Validates uploaded image files.
    """

    # ================================
    # Allowed Image Formats
    # ================================

    ALLOWED_FORMATS = {
        "JPEG",
        "PNG",
        "WEBP",
    }

    # ================================
    # Maximum File Size
    # ================================

    MAX_FILE_SIZE_MB = 20

    # ================================
    # Validate Extension
    # ================================

    @classmethod
    def validate_extension(
        cls,
        filename: str,
    ) -> bool:
        """
        Validate the file extension.
        """

        if not filename:
            return False

        extension = (
            Path(filename)
            .suffix
            .lower()
        )

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }

        return (
            extension
            in allowed_extensions
        )

    # ================================
    # Validate Image Content
    # ================================

    @classmethod
    def validate_image_content(
        cls,
        file_path: str,
    ) -> bool:
        """
        Verify that the file is
        actually a valid image.
        """

        path = Path(
            file_path
        )

        if not path.exists():
            return False

        try:

            with Image.open(
                path
            ) as image:

                image.verify()

            return True

        except Exception:

            return False

    # ================================
    # Validate File Size
    # ================================

    @classmethod
    def validate_file_size(
        cls,
        file_path: str,
    ) -> bool:
        """
        Validate maximum file size.
        """

        path = Path(
            file_path
        )

        if not path.exists():
            return False

        max_size = (
            cls.MAX_FILE_SIZE_MB
            * 1024
            * 1024
        )

        return (
            path.stat().st_size
            <= max_size
        )

    # ================================
    # Validate Complete File
    # ================================

    @classmethod
    def validate(
        cls,
        file_path: str,
    ) -> dict:
        """
        Run all file validation checks.
        """

        path = Path(
            file_path
        )

        extension_valid = (
            cls.validate_extension(
                path.name
            )
        )

        content_valid = (
            cls.validate_image_content(
                str(path)
            )
        )

        size_valid = (
            cls.validate_file_size(
                str(path)
            )
        )

        is_valid = (
            extension_valid
            and content_valid
            and size_valid
        )

        return {
            "valid": is_valid,
            "filename": path.name,
            "extension_valid": (
                extension_valid
            ),
            "content_valid": (
                content_valid
            ),
            "size_valid": (
                size_valid
            ),
        }
