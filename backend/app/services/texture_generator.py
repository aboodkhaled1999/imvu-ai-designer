from pathlib import Path
from typing import Tuple

from PIL import Image, ImageEnhance, ImageFilter


class TextureGenerator:
    """
    Handles clothing texture processing
    and prepares images for the IMVU workflow.
    """

    def __init__(
        self,
        output_dir: str = "textures",
    ):
        self.output_dir = Path(
            output_dir
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # ================================
    # Load Image
    # ================================

    def load_image(
        self,
        image_path: str,
    ) -> Image.Image:
        """
        Load an image from disk.
        """

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {image_path}"
            )

        image = Image.open(path)

        return image.convert("RGBA")

    # ================================
    # Resize Image
    # ================================

    def resize_image(
        self,
        image: Image.Image,
        size: Tuple[int, int] = (
            512,
            512,
        ),
    ) -> Image.Image:
        """
        Resize image to the requested
        texture dimensions.
        """

        return image.resize(
            size,
            Image.Resampling.LANCZOS,
        )

    # ================================
    # Enhance Texture
    # ================================

    def enhance_texture(
        self,
        image: Image.Image,
        sharpness: float = 1.5,
        contrast: float = 1.1,
    ) -> Image.Image:
        """
        Improve texture sharpness
        and contrast.
        """

        enhanced = ImageEnhance.Sharpness(
            image
        ).enhance(
            sharpness
        )

        enhanced = ImageEnhance.Contrast(
            enhanced
        ).enhance(
            contrast
        )

        return enhanced

    # ================================
    # Smooth Texture
    # ================================

    def smooth_texture(
        self,
        image: Image.Image,
    ) -> Image.Image:
        """
        Apply a light smoothing filter.
        """

        return image.filter(
            ImageFilter.SMOOTH
        )

    # ================================
    # Generate Texture
    # ================================

    def generate(
        self,
        image_path: str,
        filename: str = "generated_texture.png",
        size: Tuple[int, int] = (
            512,
            512,
        ),
    ) -> str:
        """
        Generate a processed texture.

        Steps:
        1. Load image
        2. Resize image
        3. Enhance texture
        4. Save PNG
        """

        image = self.load_image(
            image_path
        )

        image = self.resize_image(
            image,
            size,
        )

        image = self.enhance_texture(
            image
        )

        output_path = (
            self.output_dir
            / filename
        )

        image.save(
            output_path,
            format="PNG",
            optimize=True,
        )

        return str(
            output_path
        )
