from dataclasses import FrozenInstanceError
from typing import cast

import pytest

from creatorflow.domain.exceptions import InvalidConversionOptionsError
from creatorflow.domain.image import (
    ConversionOptions,
    ConversionResult,
    ImageFormat,
)


def test_image_format_values() -> None:
    assert ImageFormat.JPEG.value == "jpeg"
    assert ImageFormat.WEBP.value == "webp"
    assert ImageFormat.PNG.value == "png"


def test_image_format_is_str() -> None:
    for image_format in ImageFormat:
        assert isinstance(image_format, str)


def test_image_format_iteration() -> None:
    formats = list(ImageFormat)

    assert len(formats) == 3
    assert set(formats) == {
        ImageFormat.JPEG,
        ImageFormat.PNG,
        ImageFormat.WEBP,
    }


def test_unsupported_image_format() -> None:
    with pytest.raises(ValueError):
        ImageFormat("gif")


def test_default_options() -> None:
    options = ConversionOptions(target_format=ImageFormat.JPEG)

    assert options.target_format == ImageFormat.JPEG
    assert options.quality == 85
    assert options.background_color == (255, 255, 255)


@pytest.mark.parametrize(
    "image_format",
    [
        ImageFormat.JPEG,
        ImageFormat.PNG,
        ImageFormat.WEBP,
    ],
)
def test_valid_target_formats(image_format: ImageFormat) -> None:
    options = ConversionOptions(target_format=image_format)

    assert options.target_format == image_format


@pytest.mark.parametrize("quality", [1, 50, 85, 100])
def test_valid_quality(quality: int) -> None:
    options = ConversionOptions(
        target_format=ImageFormat.JPEG,
        quality=quality,
    )

    assert options.quality == quality


@pytest.mark.parametrize(
    "background_color",
    [
        (0, 0, 0),
        (255, 255, 255),
        (128, 64, 32),
    ],
)
def test_valid_background_color(
    background_color: tuple[int, int, int],
) -> None:
    options = ConversionOptions(
        target_format=ImageFormat.JPEG,
        background_color=background_color,
    )

    assert options.background_color == background_color


@pytest.mark.parametrize(("quality"), [0, 101, -1, True, False, 85.5, "85", None])
def test_invalid_quality(quality: object) -> None:
    with pytest.raises(InvalidConversionOptionsError):
        ConversionOptions(target_format=ImageFormat.JPEG, quality=cast(int, quality))


@pytest.mark.parametrize(
    "background_color",
    [
        (256, 0, 0),
        (-1, 0, 0),
        (255, 255),
        (255, 255, 255, 255),
        (True, 0, 0),
        (255.0, 0, 0),
        "white",
        [255, 255, 255],
        None,
    ],
)
def test_invalid_background_color(background_color: object) -> None:
    with pytest.raises(InvalidConversionOptionsError):
        ConversionOptions(
            target_format=ImageFormat.JPEG,
            background_color=cast(tuple[int, int, int], background_color),
        )


@pytest.mark.parametrize(("target_format"), ["jpeg", "gif", None, 123])
def test_invalid_target_format(target_format: object) -> None:
    with pytest.raises(InvalidConversionOptionsError):
        ConversionOptions(target_format=cast(ImageFormat, target_format))


def test_conversion_options_immutable() -> None:
    options = ConversionOptions(target_format=ImageFormat.JPEG)
    with pytest.raises(FrozenInstanceError):
        options.quality = 55  # type: ignore[misc]


def test_conversion_result_immutable() -> None:
    options = ConversionResult(
        data=b"test_bytes", format=ImageFormat.JPEG, content_type="test_content_type"
    )
    with pytest.raises(FrozenInstanceError):
        options.data = b"other_test_bytes"  # type: ignore[misc]


def test_conversion_datas_result() -> None:
    options = ConversionResult(
        data=b"test_bytes", format=ImageFormat.JPEG, content_type="test_content_type"
    )
    assert options.data == b"test_bytes"
    assert options.format == ImageFormat.JPEG
    assert options.content_type == "test_content_type"
