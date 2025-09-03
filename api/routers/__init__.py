from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.configuration.config import settings as app_settings
from api.routers import activity, admin, notification, reference


def init(app: FastAPI) -> None:
    router = APIRouter(prefix=app_settings.PREFIX)
    modules = [activity, admin, notification, reference]
    for module in modules:
        router.include_router(module.site_router)
    app.include_router(router)


__all__ = ("init",)
