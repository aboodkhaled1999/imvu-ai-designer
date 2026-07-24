from pathlib import Path
from uuid import uuid4

from PIL import Image
from rembg import remove


class BackgroundRemover:
    """
    Removes the background from clothing images
    using the rembg AI segmentation model.
    """

    def __init__(
        self,
        output_dir: str = "uploads/processed",
    ):
        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ================================
    # Validate Input
    # ================================

    def validate_input(
        self,
        image_path: str,
    ) -> Path:
        """
        Validate that the input image exists.
        """

        path = Path(
            image_path
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Input image not found: {image_path}"
            )

        return path

    # ================================
    # Remove Background
    # ================================

    def remove_background(
        self,
        image_path: str,
        output_filename: str | None = None,
    ) -> str:
        """
        Remove the background from an image.

        The result is saved as a transparent PNG.
        """

        input_path = self.validate_input(
            image_path
        )

        # Generate unique output filename
        if not output_filename:

            output_filename = (
                f"no_background_"
                f"{uuid4().hex}.png"
            )

        output_path = (
            self.output_dir
            / output_filename
        )

        # Open input image
        with Image.open(
            input_path
        ) as image:

            # Convert to RGBA
            image = image.convert(
                "RGBA"
            )

            # Remove background using AI
            result = remove(
                image
            )

            # Save transparent PNG
            result.save(
                output_path,
                format="PNG",
            )

        return str(
            output_path
        )

    # ================================
    # Process Image
    # ================================

    def process(
        self,
        image_path: str,
    ) -> dict:
        """
        Process an image and return
        information about the result.
        """

        output_path = (
            self.remove_background(
                image_path
            )
        )

        return {
            "success": True,
            "message": (
                "Background removed successfully."
            ),
            "output_path": output_path,
            "format": "PNG",
            "transparent": True,
        }
