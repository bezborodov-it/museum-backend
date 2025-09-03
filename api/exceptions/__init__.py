from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import IntegrityError
from api.cruds.base import NotFoundError
from api.dependencies.image import ImageUploadError


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(NotFoundError)
    async def model_not_found_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"{exc.model.title()} with {exc.field}={exc.value} not found"
            },
        )

    @app.exception_handler(ImageUploadError)
    async def image_upload_error(request: Request, exc: ImageUploadError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"{exc.detail}",
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request, exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(ResponseValidationError)
    async def validation_exception_handler(
            request: Request, exc: ResponseValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
        )

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError):
        return JSONResponse(
            status_code=400,
            content={
                "message": "Error: Integrity constraint violation",
                "detail": f"{exc.orig}",
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={"message": "Internal Server Error", "detail": str(exc)},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
            request: Request, exc: RequestValidationError
    ):
        error_details = []
        for error in exc.errors():
            error_detail = {
                "loc": error["loc"],
                "msg": error["msg"],
                "type": error["type"]
            }
            if "input" in error:
                error_detail["input"] = error["input"]
            error_details.append(error_detail)

        return JSONResponse(
            status_code=400,
            content={"detail": error_details},
        )
