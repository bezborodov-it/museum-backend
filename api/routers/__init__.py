from fastapi import Depends, FastAPI
from fastapi.routing import APIRouter

from api.configuration.config import settings as app_settings
from api.routers import auth, user, event, ticket, admin, notification


def init(app: FastAPI) -> None:
    router = APIRouter(prefix=app_settings.PREFIX)
    modules = [auth, admin, user, event, ticket, notification]
    for module in modules:
        router.include_router(module.site_router)
    app.include_router(router)


__all__ = ("init",)
