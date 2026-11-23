import io
from contextlib import nullcontext

from PIL import Image

from creatorflow.domain.exceptions import ImageConversionError, InvalidImageError
from creatorflow.domain.image import (
    ConversionOptions,
    ConversionResult,
    ImageConverter,
    ImageFormat,
)
from creatorflow.services.image_validator import validate_image


class PillowImageConverter(ImageConverter):
    def convert_image(
        self,
        data: bytes,
        options: ConversionOptions,
    ) -> ConversionResult:
        validate_image(data)

        target_format = options.target_format

        with io.BytesIO(data) as source, io.BytesIO() as output:
            try:
                with Image.open(source) as image:
                    try:
                        image.load()
                    except OSError as exc:
                        raise InvalidImageError from exc

                    has_transparency = (
                        image.mode in ("RGBA", "LA") or "transparency" in image.info
                    )
                    try:
                        if target_format is ImageFormat.JPEG and has_transparency:
                            rgba_context = (
                                nullcontext(image)
                                if image.mode == "RGBA"
                                else image.convert("RGBA")
                            )
                            with rgba_context as rgba:
                                with Image.new(
                                    "RGB", rgba.size, options.background_color
                                ) as background:
                                    background.paste(rgba, mask=rgba)
                                    background.save(
                                        output, format="JPEG", quality=options.quality
                                    )

                        elif target_format is ImageFormat.JPEG and image.mode == "P":
                            with image.convert("RGB") as rgb_image:
                                rgb_image.save(
                                    output, format="JPEG", quality=options.quality
                                )

                        elif target_format is ImageFormat.PNG:
                            if image.mode == "CMYK":
                                with image.convert("RGB") as rgb_image:
                                    rgb_image.save(output, format="PNG")
                            else:
                                image.save(output, format="PNG")

                        elif (
                            target_format is ImageFormat.WEBP
                            and has_transparency
                            and image.mode != "RGBA"
                        ):
                            with image.convert("RGBA") as rgba:
                                rgba.save(
                                    output, format="WEBP", quality=options.quality
                                )
                        else:
                            image.save(
                                output,
                                format=target_format.name,
                                quality=options.quality,
                            )
                    except OSError as exc:
                        raise ImageConversionError(
                            f"Failed to convert image to {target_format.value}"
                        ) from exc

            except OSError as exc:
                raise InvalidImageError from exc

            return ConversionResult(
                data=output.getvalue(),
                format=target_format,
                content_type=f"image/{target_format.value}",
            )
