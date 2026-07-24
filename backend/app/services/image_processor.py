from pathlib import Path
from uuid import uuid4

from app.config import settings
from app.services.background_remover import (
    BackgroundRemover,
)
from app.services.color_detector import (
    ColorDetector,
)
from app.services.texture_generator import (
    TextureGenerator,
)


class ImageProcessor:
    """
    Main image processing pipeline.

    This service combines:
    - Background removal
    - Color detection
    - Texture generation
    """

    def __init__(self):
        # ================================
        # Directory Configuration
        # ================================

        self.upload_dir = Path(
            settings.UPLOAD_DIR
        )

        self.processed_dir = (
            self.upload_dir
            / "processed"
        )

        self.texture_dir = Path(
            settings.TEXTURE_DIR
        )

        # Create directories
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.processed_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.texture_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ================================
        # Initialize Services
        # ================================

        self.background_remover = (
            BackgroundRemover(
                output_dir=str(
                    self.processed_dir
                )
            )
        )

        self.color_detector = (
            ColorDetector(
                color_count=5
            )
        )

        self.texture_generator = (
            TextureGenerator(
                output_dir=str(
                    self.texture_dir
                )
            )
        )

    # ================================
    # Validate Image
    # ================================

    def validate_image(
        self,
        image_path: str,
    ) -> Path:
        """
        Validate that an image exists.
        """

        path = Path(
            image_path
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        return path

    # ================================
    # Remove Background
    # ================================

    def process_background(
        self,
        image_path: str,
    ) -> str:
        """
        Remove the image background.
        """

        result = (
            self.background_remover.remove_background(
                image_path
            )
        )

        return result

    # ================================
    # Detect Colors
    # ================================

    def process_colors(
        self,
        image_path: str,
    ) -> dict:
        """
        Detect dominant colors.
        """

        return (
            self.color_detector.analyze(
                image_path
            )
        )

    # ================================
    # Generate Texture
    # ================================

    def process_texture(
        self,
        image_path: str,
    ) -> str:
        """
        Generate a processed texture.
        """

        filename = (
            f"texture_"
            f"{uuid4().hex}.png"
        )

        return (
            self.texture_generator.generate(
                image_path,
                filename=filename,
            )
        )

    # ================================
    # Full Processing Pipeline
    # ================================

    def process(
        self,
        image_path: str,
        remove_background: bool = True,
        detect_colors: bool = True,
        generate_texture: bool = True,
    ) -> dict:
        """
        Run the complete image processing pipeline.

        Steps:
        1. Validate image
        2. Remove background
        3. Detect colors
        4. Generate texture
        """

        input_path = (
            self.validate_image(
                image_path
            )
        )

        current_image = str(
            input_path
        )

        result = {
            "success": True,
            "input_file": str(
                input_path
            ),
            "background_removed": False,
            "colors_detected": False,
            "texture_generated": False,
            "processed_image": None,
            "colors": [],
            "texture": None,
        }

        # ================================
        # Background Removal
        # ================================

        if remove_background:

            processed_image = (
                self.process_background(
                    current_image
                )
            )

            current_image = (
                processed_image
            )

            result[
                "background_removed"
            ] = True

            result[
                "processed_image"
            ] = processed_image

        # ================================
        # Color Detection
        # ================================

        if detect_colors:

            colors = (
                self.process_colors(
                    current_image
                )
            )

            result[
                "colors_detected"
            ] = True

            result[
                "colors"
            ] = colors.get(
                "colors",
                [],
            )

        # ================================
        # Texture Generation
        # ================================

        if generate_texture:

            texture = (
                self.process_texture(
                    current_image
                )
            )

            result[
                "texture_generated"
            ] = True

            result[
                "texture"
            ] = texture

        return result
