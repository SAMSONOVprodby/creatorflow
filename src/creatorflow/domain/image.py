from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from creatorflow.domain.exceptions import InvalidConversionOptionsError


class ImageFormat(StrEnum):
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"


@dataclass(frozen=True)
class ConversionOptions:
    target_format: ImageFormat
    quality: int = 85
    background_color: tuple[int, int, int] = (255, 255, 255)

    def __post_init__(self) -> None:
        if not isinstance(self.target_format, ImageFormat):
            raise InvalidConversionOptionsError("target_format must be an ImageFormat")

        if type(self.quality) is not int or not 1 <= self.quality <= 100:
            raise InvalidConversionOptionsError(
                "quality must be an integer between 1 and 100"
            )

        if (
            not isinstance(self.background_color, tuple)
            or len(self.background_color) != 3
        ):
            raise InvalidConversionOptionsError(
                "background_color must be a tuple of 3 integers"
            )

        if not all(
            type(channel) is int and 0 <= channel <= 255
            for channel in self.background_color
        ):
            raise InvalidConversionOptionsError(
                "background_color channels must be integers between 0 and 255"
            )


@dataclass(frozen=True)
class ConversionResult:
    data: bytes
    format: ImageFormat
    content_type: str


class ImageConverter(Protocol):
    def convert_image(
        self,
        data: bytes,
        options: ConversionOptions,
    ) -> ConversionResult: ...
