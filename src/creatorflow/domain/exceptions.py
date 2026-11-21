class ImageConversionError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidImageError(ImageConversionError):
    def __init__(self, message: str = "Corrupted image or invalid data"):
        super().__init__(message)


class UnsupportedImageFormatError(ImageConversionError):
    def __init__(self, message: str = "The original format is not supported"):
        super().__init__(message)


class ImageTooLargeError(ImageConversionError):
    def __init__(self, message: str = "Size limits exceeded"):
        super().__init__(message)


class InvalidConversionOptionsError(ImageConversionError):
    def __init__(self, message: str = "Incorrect conversion parameters"):
        super().__init__(message)
