from io import BytesIO

from PIL import Image, UnidentifiedImageError

from creatorflow.domain.exceptions import (
    ImageTooLargeError,
    InvalidImageError,
    UnsupportedImageFormatError,
)
from creatorflow.domain.image import ImageFormat

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000


def validate_image(data: bytes) -> ImageFormat:
    if not isinstance(data, bytes):
        raise InvalidImageError

    if not data:
        raise InvalidImageError

    if len(data) > MAX_IMAGE_SIZE_BYTES:
        raise ImageTooLargeError

    try:
        with Image.open(BytesIO(data)) as img:
            width, height = img.size
            if width <= 0 or height <= 0:
                raise InvalidImageError
            if width * height > MAX_IMAGE_PIXELS:
                raise ImageTooLargeError

            if getattr(img, "is_animated", False) or getattr(img, "n_frames", 1) > 1:
                raise UnsupportedImageFormatError

            real_format = img.format
            if real_format is None:
                raise InvalidImageError
            try:
                image_format = ImageFormat(real_format.lower())
            except ValueError as exc:
                raise UnsupportedImageFormatError from exc

            img.verify()

    except Image.DecompressionBombError as exc:
        raise ImageTooLargeError from exc
    except (UnidentifiedImageError, OSError) as exc:
        raise InvalidImageError from exc

    try:
        with Image.open(BytesIO(data)) as img:
            img.load()

    except Image.DecompressionBombError as exc:
        raise ImageTooLargeError from exc
    except (UnidentifiedImageError, OSError) as exc:
        raise InvalidImageError from exc

    return image_format
