import os
from io import BytesIO
from unittest.mock import MagicMock

import pytest
from PIL import Image

from creatorflow.domain.exceptions import (
    ImageTooLargeError,
    InvalidImageError,
    UnsupportedImageFormatError,
)
from creatorflow.domain.image import ImageFormat
from creatorflow.services.image_validator import validate_image, MAX_IMAGE_SIZE_BYTES


@pytest.mark.parametrize("format", ["jpeg", "png", "webp"])
def test_valid_image(format) -> None:
    img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format)
    raw_bytes = buffer.getvalue()
    image_format = validate_image(raw_bytes)
    assert image_format == ImageFormat(format)


def test_empty_image() -> None:
    with pytest.raises(InvalidImageError):
        validate_image(b"")


@pytest.mark.parametrize(
    "data", [None, "test_data", ["test_data1", "test_data2"], bytearray(b"test_data")]
)
def test_invalid_data_type(data) -> None:
    with pytest.raises(InvalidImageError):
        validate_image(data)


def test_random_bytes() -> None:
    random_bytes = os.urandom(16)
    with pytest.raises(InvalidImageError):
        validate_image(random_bytes)


@pytest.mark.parametrize("format", ["gif", "bmp"])
def test_unsupported_format(format) -> None:
    img = Image.new("RGB", (1000, 1000), color=(255, 255, 255))
    buffer = BytesIO()
    img.save(buffer, format)
    raw_bytes = buffer.getvalue()
    with pytest.raises(UnsupportedImageFormatError):
        validate_image(raw_bytes)


def test_file_too_large() -> None:
    data = b"\x00" * (MAX_IMAGE_SIZE_BYTES + 1)

    with pytest.raises(ImageTooLargeError):
        validate_image(data)


def test_pixel_limit(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_image = MagicMock()
    fake_image.size = (5001, 5001)

    fake_image.__enter__.return_value = fake_image

    def fake_open(*args, **kwargs):
        return fake_image

    monkeypatch.setattr(
        "creatorflow.services.image_validator.Image.open",
        fake_open,
    )

    with pytest.raises(ImageTooLargeError):
        validate_image(b"test")


def test_pixel_limit_boundary(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_image = MagicMock()

    fake_image.size = (5000, 5000)
    fake_image.format = "png"
    fake_image.is_animated = False
    fake_image.n_frames = 1

    fake_image.__enter__.return_value = fake_image

    def fake_open(*args, **kwargs):
        return fake_image

    monkeypatch.setattr(
        "creatorflow.services.image_validator.Image.open",
        fake_open,
    )

    result = validate_image(b"test")

    assert result == ImageFormat.PNG
    fake_image.verify.assert_called_once()
    fake_image.load.assert_called_once()


def test_animated_image() -> None:
    frames = [Image.new("RGB", (1, 1), color=color) for color in ("red", "blue")]
    buffer = BytesIO()
    frames[0].save(
        buffer,
        format="WEBP",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
    )
    raw_bytes = buffer.getvalue()
    with pytest.raises(UnsupportedImageFormatError):
        validate_image(raw_bytes)


@pytest.mark.parametrize("image_format", ["jpeg", "png"])
def test_truncated_image(image_format) -> None:
    buffer = BytesIO()
    img = Image.new("RGB", (100, 100), color=(255, 255, 255))
    img.save(buffer, image_format)
    raw_bytes = buffer.getvalue()
    truncated_bytes = raw_bytes[: len(raw_bytes) // 2]
    with pytest.raises(InvalidImageError):
        validate_image(truncated_bytes)

def test_load_oserror(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_image = MagicMock()

    fake_image.size = (100, 100)
    fake_image.format = "PNG"
    fake_image.is_animated = False
    fake_image.n_frames = 1

    fake_image.__enter__.return_value = fake_image

    fake_image.load.side_effect = OSError("Failed to decode image")

    def fake_open(*args, **kwargs):
        return fake_image

    monkeypatch.setattr(
        "creatorflow.services.image_validator.Image.open",
        fake_open,
    )

    with pytest.raises(InvalidImageError) as exc_info:
        validate_image(b"test")

    assert isinstance(exc_info.value.__cause__, OSError)

    fake_image.verify.assert_called_once()
    fake_image.load.assert_called_once()