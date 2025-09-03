from fastapi import APIRouter, Depends, status, Response, Path, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import PositiveInt
from typing import Optional

from api import schemas
from api.cruds import Event, Exhibition
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_basic_user, get_image_with
from api.models import UserORM
from api.utils.image import save_image

site_router = APIRouter(prefix="/admin", tags=["admin"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/events",
    tags=["event"],
    status_code=200,
    response_model=schemas.EventsAdminGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_admin_events(
    search: Optional[str] = Query(None, description="Search string"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, gt=0, le=100, description="Limit"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events, total_count = await Event.get_admin_list(
        session,
        search,
        offset,
        limit,
    )
    return schemas.EventsAdminGet(items=events, total=total_count)


@site_router.post(
    "/event",
    tags=["event"],
    response_model=schemas.EventBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_event(
    payload: schemas.EventCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(get_basic_user),
) -> Response:
    event = await Event.create(session, payload.model_dump())
    return event


@site_router.patch(
    "/event/{event_id}",
    response_model=schemas.EventBase,
    tags=["event"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_event_by_id(
    payload: schemas.EventUpdate,
    event_id: PositiveInt = Path(..., description="The identifier of event"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    event = await Event.update(session, event_id, payload.model_dump())
    return event


@site_router.delete(
    "/event/{event_id}",
    status_code=204,
    tags=["event"],
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_event_by_id(
    event_id: PositiveInt = Path(..., description="The identifier of event"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Event.delete(session, event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/event/{event_id}/upload_logo",
    status_code=200,
    response_model=schemas.EventBase,
    tags=["event"],
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_logo_by_event_id(
    event_id: PositiveInt = Path(..., description="The identifier of event"),
    file: UploadFile = Depends(get_image_with),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    event = await Event.update_image_url(session, event_id, image_url)
    return event


@site_router.post(
    "/exhibition",
    tags=["exhibition"],
    response_model=schemas.ExhibitionBase,
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_exhibition(
    payload: schemas.ExhibitionCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(get_basic_user),
) -> Response:
    exhibition = await Exhibition.create(session, payload.model_dump())
    return schemas.ExhibitionBase.model_validate(exhibition)


@site_router.get(
    "/exhibitions",
    tags=["exhibition"],
    status_code=200,
    response_model=schemas.ExhibitionsAdminGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_admin_exhibitions(
    search: Optional[str] = Query(None, description="Search string"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, gt=0, le=100, description="Limit"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibitions, total_count = await Exhibition.get_admin_list(
        session,
        search,
        offset,
        limit,
    )
    return schemas.ExhibitionsAdminGet(items=exhibitions, total=total_count)


@site_router.patch(
    "/exhibition/{exhibition_id}",
    response_model=schemas.ExhibitionBase,
    tags=["exhibition"],
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_exhibition_by_id(
    pyload: schemas.ExhibitionUpdate,
    exhibition_id: PositiveInt = Path(..., description="The identifier of exhibition"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibition = await Exhibition.update(session, exhibition_id, pyload.model_dump())
    return exhibition


@site_router.delete(
    "/exhibition/{exhibition_id}",
    tags=["exhibition"],
    status_code=204,
    responses={
        200: {"description": "Success"},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def delete_exhibition_by_id(
    exhibition_id: PositiveInt = Path(..., description="The identifier of event"),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    await Exhibition.delete(session, exhibition_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/exhibition/{exhibition_id}/upload_logo",
    status_code=200,
    tags=["exhibition"],
    response_model=schemas.ExhibitionBase,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def upload_logo_by_exhibition_id(
    exhibition_id: PositiveInt = Path(..., description="The identifier of exhibition"),
    file: UploadFile = Depends(get_image_with),
    current_user: UserORM = Depends(get_basic_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    image_url = save_image(file)
    exhibition = await Exhibition.update_image_url(session, exhibition_id, image_url)
    return exhibition
