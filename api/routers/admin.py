from fastapi import APIRouter, Depends, HTTPException, status, Response, Path, UploadFile, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
from pydantic import PositiveInt
from typing import List

from api import schemas
from api.cruds import Event, Ticket
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_basic_user, is_admin, get_image_with
from api.models import UserORM
from api.utils.image import save_event_image

site_router = APIRouter(prefix="/admin", tags=["admin"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/event/all",
    status_code=200,
    response_model=schemas.EventsAdminGet,
    responses=response_codes,
)
async def get_admin_events(
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events, total_count = await Event.get_admin(
        session,
        offset,
        limit,
    )
    return {
        "items": events,
        "total": total_count,
    }


@site_router.post(
    "/event",
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
    new_event = await Event.create(session, payload.dict())
    return new_event


@site_router.get(
    "/event/{event_id}",
    response_model=schemas.EventAdminGet,
    status_code=200,
    responses=response_codes,
)
async def get_admin_event_by_id(
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    event, ticket_available, ticket_booked, ticket_sold = await Event.get_admin_event_by_id(session, event_id)
    return schemas.EventAdminGet(
        event=event,
        ticket_available=ticket_available,
        ticket_booked=ticket_booked,
        ticket_sold=ticket_sold,
    )


@site_router.put(
    "/event/{event_id}",
    response_model=schemas.EventBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def update_event_by_id(
        pyload: schemas.EventUpdate,
        event_id: PositiveInt = Path(..., description="The identifier of event"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    updated_event = await Event.update(
        session, event_id, pyload.dict(exclude_unset=True)
    )
    return updated_event


@site_router.post(
    "/event/{event_id}/upload_logo",
    status_code=200,
    response_model=schemas.EventBase,
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
    image_url = save_event_image(file)
    updated_event = await Event.update_image_url(session, event_id, image_url)
    return updated_event


@site_router.delete(
    "/event/{event_id}",
    status_code=204,
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
    await Event.delete(
        session, event_id
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@site_router.post(
    "/ticket",
    response_model=List[schemas.TicketBase],
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_tickets(
        payload: schemas.TicketCreate,
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    tickets = await Ticket.create_bulk(session, payload.dict())
    return tickets
