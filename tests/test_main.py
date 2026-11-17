from fastapi import FastAPI

from creatorflow.core.config import Settings
from creatorflow.main import create_app


def test_create_app() -> None:
    settings = Settings()

    app = create_app(settings)

    assert isinstance(app, FastAPI)


def test_difference_apps() -> None:
    settings = Settings()

    app1 = create_app(settings)
    app2 = create_app(settings)

    assert app1 is not app2


def test_title_app() -> None:
    title: str = "Example"

    settings = Settings(app_name=title)

    app = create_app(settings)

    assert app.title == title


def test_version_app() -> None:
    version: str = "0.0.0"

    settings = Settings(app_version=version)

    app = create_app(settings)

    assert app.version == version


def test_debug_app() -> None:
    debug: bool = True

    settings = Settings(debug=debug)

    app = create_app(settings)

    assert app.debug == debug
