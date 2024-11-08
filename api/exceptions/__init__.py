from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from sqlalchemy.exc import NoResultFound, IntegrityError
from api.cruds.base import ModelNotFoundError
from api.dependencies.image import ImageUploadError
from api.exceptions.base import TicketNotAvailableError


def init_exception_handlers(app: FastAPI):
    @app.exception_handler(ModelNotFoundError)
    async def model_not_found_handler(request: Request, exc: ModelNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"{exc.model.title()} not found",
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

    @app.exception_handler(TicketNotAvailableError)
    async def ticket_not_available_handler(
        request: Request, exc: TicketNotAvailableError
    ):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.message,
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
