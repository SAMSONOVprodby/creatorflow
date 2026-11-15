def normalize_extension(extension: str) -> str:

    if not extension:
        return ""

    extension = extension.strip()

    if extension.startswith("."):
        extension = extension[1:]

    extension = extension.lower()

    return extension
