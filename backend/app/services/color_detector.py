from collections import Counter
from typing import List, Dict, Tuple

import numpy as np
from PIL import Image


class ColorDetector:
    """
    Detects the dominant colors in a clothing image.
    """

    def __init__(
        self,
        color_count: int = 5,
    ):
        self.color_count = color_count

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

        image = Image.open(
            image_path
        )

        return image.convert(
            "RGB"
        )

    # ================================
    # Resize For Analysis
    # ================================

    def prepare_image(
        self,
        image: Image.Image,
        size: Tuple[int, int] = (
            100,
            100,
        ),
    ) -> Image.Image:
        """
        Resize image to reduce
        processing requirements.
        """

        return image.resize(
            size,
            Image.Resampling.LANCZOS,
        )

    # ================================
    # Extract Dominant Colors
    # ================================

    def detect_colors(
        self,
        image: Image.Image,
    ) -> List[Dict]:
        """
        Detect dominant RGB colors
        in the image.
        """

        image = self.prepare_image(
            image
        )

        pixels = np.array(
            image
        )

        pixels = pixels.reshape(
            -1,
            3,
        )

        color_counter = Counter(
            map(
                tuple,
                pixels,
            )
        )

        most_common = (
            color_counter.most_common(
                self.color_count
            )
        )

        results = []

        total_pixels = len(
            pixels
        )

        for color, count in most_common:

            percentage = (
                count
                / total_pixels
            ) * 100

            results.append(
                {
                    "rgb": {
                        "r": int(
                            color[0]
                        ),
                        "g": int(
                            color[1]
                        ),
                        "b": int(
                            color[2]
                        ),
                    },
                    "percentage": round(
                        percentage,
                        2,
                    ),
                }
            )

        return results

    # ================================
    # RGB To HEX
    # ================================

    def rgb_to_hex(
        self,
        rgb: Tuple[int, int, int],
    ) -> str:
        """
        Convert RGB color to HEX.
        """

        return "#{:02X}{:02X}{:02X}".format(
            rgb[0],
            rgb[1],
            rgb[2],
        )

    # ================================
    # Analyze Image
    # ================================

    def analyze(
        self,
        image_path: str,
    ) -> Dict:
        """
        Analyze the image and return
        dominant colors in RGB and HEX.
        """

        image = self.load_image(
            image_path
        )

        colors = self.detect_colors(
            image
        )

        for item in colors:

            rgb = (
                item["rgb"]["r"],
                item["rgb"]["g"],
                item["rgb"]["b"],
            )

            item["hex"] = (
                self.rgb_to_hex(
                    rgb
                )
            )

        return {
            "success": True,
            "color_count": len(
                colors
            ),
            "colors": colors,
        }
