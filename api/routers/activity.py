from fastapi import (
    APIRouter,
    Depends,
    Response,
    Path,
    Query,
)
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import (
    Event,
    Exhibition,
    PushToken,
)
from api.configuration.database.db_helper import db_helper

site_router = APIRouter(prefix="/activity", tags=["activity"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/events",
    status_code=200,
    response_model=schemas.EventFilterGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_events(
    genre_ids: List[int] = Query(None, description="Genre"),
    location_ids: List[int] = Query(None, description="Location"),
    visitor_category_ids: List[int] = Query(None, description="Visitor category"),
    category_ids: List[int] = Query(None, description="Category"),
    disabilities: bool = Query(None, description="Disabilities"),
    is_free: bool = Query(None, description="Is free"),
    pushkin_card: bool = Query(None, description="Pay by pushkin card"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, gt=0, le=100, description="Limit"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events, total_count = await Event.filter(
        session,
        genre_ids,
        location_ids,
        visitor_category_ids,
        category_ids,
        disabilities,
        is_free,
        pushkin_card,
        offset,
        limit,
    )
    return schemas.EventFilterGet(items=events, total=total_count)


@site_router.get(
    "/event/{event_id}",
    response_model=schemas.EventBase,
    status_code=200,
    responses=response_codes,
)
async def get_event_by_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    event_id: PositiveInt = Path(..., description="The identifier of event"),
) -> Response:
    event = await Event.get_by_id(session, event_id)
    return event


@site_router.get(
    "/exhibitions",
    status_code=200,
    response_model=schemas.ExhibitionFilterGet,
    responses={
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def get_exhibitions(
    genre: List[int] = Query(None, description="Genre"),
    location: List[int] = Query(None, description="Location"),
    visitor_category: List[int] = Query(None, description="Visitor category"),
    category: List[int] = Query(None, description="Category"),
    disabilities: bool = Query(None, description="Disabilities"),
    is_free: bool = Query(None, description="Is free"),
    pushkin_card: bool = Query(None, description="Pay by pushkin card"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, gt=0, le=100, description="Limit"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibitions, total_count = await Exhibition.filter(
        session,
        genre,
        location,
        visitor_category,
        category,
        disabilities,
        is_free,
        pushkin_card,
        offset,
        limit,
    )
    return schemas.ExhibitionFilterGet(items=exhibitions, total=total_count)


@site_router.get(
    "/exhibition/{exhibition_id}",
    response_model=schemas.ExhibitionBase,
    status_code=200,
    responses=response_codes,
)
async def get_exhibition_by_id(
    exhibition_id: PositiveInt = Path(..., description="The identifier of exhibition"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibition = await Exhibition.get_by_id(session, exhibition_id)
    return exhibition


@site_router.post(
    "/preference",
    response_model=schemas.ActivityPreferencesGet,
    status_code=201,
    responses=response_codes,
)
async def create_preference(
    payload: schemas.ActivityPreferencesCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    push_token_obj = await PushToken.create_preference(
        session,
        payload.push_token,
        payload.tags,
        payload.genres,
        payload.visitor_categories,
    )

    events = await Event.get_by_preferences(session, push_token_obj)
    exhibitions = await Exhibition.get_by_preferences(session, push_token_obj)

    return schemas.ActivityPreferencesGet(events=events, exhibitions=exhibitions)


@site_router.get(
    "/preferences",
    response_model=schemas.ActivityPreferencesGet,
    status_code=200,
    responses=response_codes,
)
async def get_preferences(
    push_token: str = Query(..., description="Push token string"),
    limit: int = Query(3, gt=0, le=6, description="Limit by each category"),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    push_token_obj = await PushToken.get_by_token(session, push_token)

    events = await Event.get_by_preferences(session, push_token_obj, limit)
    exhibitions = await Exhibition.get_by_preferences(session, push_token_obj, limit)

    return schemas.ActivityPreferencesGet(events=events, exhibitions=exhibitions)
