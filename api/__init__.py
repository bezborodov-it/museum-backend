import os
from fastapi import FastAPI, Request
from typing import Optional, Awaitable, Callable, AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from starlette.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from api.configuration.config import settings
from api.configuration.database import disconnect_db
from api.exceptions import init_exception_handlers

_app: Optional[FastAPI] = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    yield
    # Shutdown
    await disconnect_db()


def _init_app() -> FastAPI:
    from .routers import init as init_routers

    app = FastAPI(
        lifespan=lifespan,
        title="MUSEUM API",
        description="API for MUSEUM",
        version=settings.VERSION,
        openapi_url=f"{settings.PREFIX}/openapi.json",
        docs_url=f"{settings.PREFIX}/docs",
        redoc_url=f"{settings.PREFIX}/redoc",
    )

    app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

    if len(settings.CORS_ORIGINS) > 0 or settings.CORS_ORIGIN_REGEX is not None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
            allow_origin_regex=settings.CORS_ORIGIN_REGEX,
        )

    init_routers(app)
    init_exception_handlers(app)
    return app


def get_app() -> FastAPI:
    global _app

    if _app is None:
        _app = _init_app()
    return _app
