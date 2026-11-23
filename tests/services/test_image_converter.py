import io

import pytest
from PIL import Image, PngImagePlugin

from creatorflow.domain.exceptions import ImageConversionError, InvalidImageError
from creatorflow.domain.image import ConversionOptions, ImageConverter, ImageFormat
from creatorflow.services import image_converter
from creatorflow.services.image_converter import PillowImageConverter


@pytest.mark.parametrize("source_format", list(ImageFormat))
@pytest.mark.parametrize("target_format", list(ImageFormat))
def test_convert_rgb_image(
    source_format: ImageFormat, target_format: ImageFormat
) -> None:
    size = (32, 24)

    with io.BytesIO() as source, Image.new("RGB", size, "red") as image:
        image.save(source, format=source_format.name)
        data = source.getvalue()

    converter: ImageConverter = PillowImageConverter()
    options = ConversionOptions(target_format=target_format, quality=85)

    result = converter.convert_image(data, options)

    assert result.format is target_format
    assert result.content_type == f"image/{target_format.value}"

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        converted.load()
        assert converted.format == target_format.name
        assert converted.size == size


def test_cmyk_rgb_image() -> None:
    size = (32, 24)

    with io.BytesIO() as source, Image.new("CMYK", size, (0, 255, 255, 0)) as image:
        image.save(source, format="JPEG")
        data = source.getvalue()

    converter: ImageConverter = PillowImageConverter()
    options = ConversionOptions(target_format=ImageFormat.PNG)

    result = converter.convert_image(data, options)

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        converted.load()
        assert converted.mode == "RGB"
        assert converted.format == "PNG"
        assert converted.size == size


def test_convert_rgba_png_to_jpeg_with_background() -> None:
    size = (32, 24)
    foreground = (255, 0, 0, 128)

    with io.BytesIO() as source, Image.new("RGBA", size, foreground) as image:
        image.save(source, format="PNG")
        data = source.getvalue()

    converter: ImageConverter = PillowImageConverter()
    options = ConversionOptions(
        target_format=ImageFormat.JPEG,
        quality=100,
        background_color=(0, 0, 255),
    )

    result = converter.convert_image(data, options)

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        assert converted.format == "JPEG"
        assert converted.mode == "RGB"
        assert converted.size == size
        assert converted.getpixel((16, 12)) == pytest.approx((128, 0, 127), abs=3)


@pytest.mark.parametrize(
    ("mode", "color", "transparency", "expected_pixel"),
    [
        pytest.param(
            "LA",
            (200, 128),
            None,
            (100, 100, 227),
            id="grayscale-with-alpha",
        ),
        pytest.param(
            "P",
            0,
            0,
            (0, 0, 255),
            id="transparent-palette-index-zero",
        ),
        pytest.param(
            "RGB",
            (255, 0, 0),
            (255, 0, 0),
            (0, 0, 255),
            id="transparent-rgb-color",
        ),
    ],
)
def test_convert_transparent_png_to_jpeg(
    mode: str,
    color: int | tuple[int, ...],
    transparency: int | tuple[int, int, int] | None,
    expected_pixel: tuple[int, int, int],
) -> None:
    size = (32, 24)

    with io.BytesIO() as source, Image.new(mode, size, color) as image:
        if transparency is not None:
            image.info["transparency"] = transparency

        image.save(source, format="PNG")
        data = source.getvalue()

    options = ConversionOptions(
        target_format=ImageFormat.JPEG,
        quality=100,
        background_color=(0, 0, 255),
    )
    result = PillowImageConverter().convert_image(data, options)

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        assert converted.format == "JPEG"
        assert converted.mode == "RGB"
        assert converted.size == size
        assert converted.getpixel((16, 12)) == pytest.approx(expected_pixel, abs=3)


@pytest.mark.parametrize(
    "target_format", [ImageFormat.PNG, ImageFormat.WEBP], ids=["png", "webp"]
)
@pytest.mark.parametrize(
    ("mode", "color", "transparency", "expected_alpha"),
    [
        pytest.param("RGBA", (255, 0, 0, 128), None, 128, id="rgba-alpha"),
        pytest.param(
            "RGB",
            (255, 0, 0),
            (255, 0, 0),
            0,
            id="rgb-transparent-color",
        ),
    ],
)
def test_convert_png_preserves_transparency(
    target_format: ImageFormat,
    mode: str,
    color: tuple[int, ...],
    transparency: tuple[int, int, int] | None,
    expected_alpha: int,
) -> None:
    size = (32, 24)

    with io.BytesIO() as source, Image.new(mode, size, color) as image:
        if transparency is not None:
            image.info["transparency"] = transparency
        image.save(source, format="PNG")
        data = source.getvalue()

    options = ConversionOptions(target_format)
    result = PillowImageConverter().convert_image(data, options)

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        assert converted.format == target_format.name
        assert converted.size == size

        with converted.convert("RGBA") as rgba:
            assert rgba.getpixel((16, 12))[3] == expected_alpha


def test_convert_image_wraps_decode_error(
    monkeypatch: pytest.MonkeyPatch, valid_png_bytes: bytes
) -> None:
    decode_error = OSError("Simulated PNG decoding failure")

    def fail_load(_image: PngImagePlugin.PngImageFile) -> None:
        raise decode_error

    monkeypatch.setattr(
        image_converter, "validate_image", lambda _data: ImageFormat.PNG
    )
    monkeypatch.setattr(PngImagePlugin.PngImageFile, "load", fail_load)

    options = ConversionOptions(target_format=ImageFormat.JPEG)

    with pytest.raises(InvalidImageError) as error:
        PillowImageConverter().convert_image(valid_png_bytes, options)

    assert error.value.__cause__ is decode_error


def test_convert_image_wraps_save_error(
    monkeypatch: pytest.MonkeyPatch,
    valid_png_bytes: bytes,
) -> None:
    save_error = OSError("Simulated JPEG encodung failure")

    def fail_save(
        _image: Image.Image,
        _output: io.BytesIO,
        **_options: object,
    ) -> None:
        raise save_error

    monkeypatch.setattr(Image.Image, "save", fail_save)

    options = ConversionOptions(target_format=ImageFormat.JPEG)

    with pytest.raises(
        ImageConversionError, match="Failed to convert image to jpeg"
    ) as error:
        PillowImageConverter().convert_image(valid_png_bytes, options)

    assert type(error.value) is ImageConversionError
    assert error.value.__cause__ is save_error


def test_convert_opaque_palette_png_to_jpeg() -> None:
    size = (32, 24)

    with io.BytesIO() as source, Image.new("P", size, 0) as image:
        image.putpalette([255, 0, 0] + [0, 0, 0] * 255)
        image.save(source, format="PNG")
        data = source.getvalue()

    options = ConversionOptions(target_format=ImageFormat.JPEG, quality=100)
    result = PillowImageConverter().convert_image(data, options)

    with io.BytesIO(result.data) as output, Image.open(output) as converted:
        assert converted.format == "JPEG"
        assert converted.mode == "RGB"
        assert converted.size == size
        assert converted.getpixel((16, 12)) == pytest.approx((255, 0, 0), abs=3)
