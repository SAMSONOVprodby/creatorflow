from fastapi import FastAPI

from creatorflow.api.router import api_router
from creatorflow.core.config import Settings


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings()

    app = FastAPI(
        title=settings.app_name, version=settings.app_version, debug=settings.debug
    )

    app.include_router(api_router)

    return app
