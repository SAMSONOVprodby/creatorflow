import pytest
from pydantic import ValidationError

from creatorflow.core.config import Settings


def test_settings_by_default(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    settings = Settings(_env_file=None)

    assert settings.app_name == "CreatorFlow"
    assert settings.app_version == "0.1.0"
    assert not settings.debug
    assert settings.environment == "development"


def test_settings_by_arg(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("APP_NAME", raising=False)
    monkeypatch.delenv("APP_VERSION", raising=False)
    monkeypatch.delenv("DEBUG", raising=False)
    monkeypatch.delenv("ENVIRONMENT", raising=False)

    settings = Settings(
        app_name="TestApp",
        app_version="0.0.0",
        debug=True,
        environment="testing",
        _env_file=None,
    )

    assert settings.app_name == "TestApp"
    assert settings.app_version == "0.0.0"
    assert settings.debug
    assert settings.environment == "testing"


def test_settings_by_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "EnvironmentApp")

    settings = Settings(_env_file=None)

    assert settings.app_name == "EnvironmentApp"


def test_settings_invalid_environment() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="invalid", _env_file=None)
