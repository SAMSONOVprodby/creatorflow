import pytest

from creatorflow.utils.filenames import normalize_extension


@pytest.mark.parametrize(
    ("extension", "expected"),
    [
        (".MP4", "mp4"),
        (" .JPG ", "jpg"),
        ("png", "png"),
        ("  .PDF  ", "pdf"),
        ("", ""),
        ("   ", ""),
        ("..mp4", ".mp4"),
    ],
)
def test_normalize_extension(extension: str, expected: str) -> None:
    result = normalize_extension(extension)

    assert result == expected


@pytest.mark.parametrize(
    ("extension"),
    [
        (".MP4"),
        (" .JPG "),
        ("png"),
        ("  .PDF  "),
        (""),
        ("   "),
        ("..mp4"),
    ],
)
def test_normalize_extension_return_type(extension: str) -> None:
    result = normalize_extension(extension)

    assert isinstance(result, str)
