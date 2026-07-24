"""
Image processing utilities.

Responsible for preparing uploaded images before they are stored.

Features
--------
- Validates image files.
- Converts to RGB.
- Applies EXIF orientation.
- Center crops.
- Resizes.
- Converts to WebP.
"""

from __future__ import annotations

from io import BytesIO

from django.core.files.base import ContentFile

from PIL import Image
from PIL import ImageOps

from apps.users.constants import (
    AVATAR_OUTPUT_FORMAT,
    AVATAR_OUTPUT_QUALITY,
    AVATAR_OUTPUT_SIZE,
)


# =============================================================================
# Public API
# =============================================================================


def process_image(
    *,
    image_file,
    size: tuple[int, int] = AVATAR_OUTPUT_SIZE,
    quality: int = AVATAR_OUTPUT_QUALITY,
    output_format: str = AVATAR_OUTPUT_FORMAT,
) -> ContentFile:
    """
    Process an uploaded image.

    Workflow
    --------
        1. Open image.
        2. Apply EXIF orientation.
        3. Convert to RGB.
        4. Center crop.
        5. Resize.
        6. Convert to WebP.
        7. Return ContentFile.

    Parameters
    ----------
    image_file:
        Uploaded image.

    size:
        Output dimensions.

    quality:
        Compression quality.

    output_format:
        Output format.

    Returns
    -------
    ContentFile
    """

    # -------------------------------------------------------------------------
    # Open image
    # -------------------------------------------------------------------------

    image = Image.open(image_file)

    # -------------------------------------------------------------------------
    # Respect phone camera orientation
    # -------------------------------------------------------------------------

    image = ImageOps.exif_transpose(image)

    # -------------------------------------------------------------------------
    # Convert transparency / palette images
    # -------------------------------------------------------------------------

    if image.mode != "RGB":
        image = image.convert("RGB")

    # -------------------------------------------------------------------------
    # Center crop + resize
    # -------------------------------------------------------------------------

    image = ImageOps.fit(
        image,
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )

    # -------------------------------------------------------------------------
    # Encode
    # -------------------------------------------------------------------------

    output = BytesIO()

    image.save(
        output,
        format=output_format,
        quality=quality,
        optimize=True,
    )

    output.seek(0)

    return ContentFile(output.read())