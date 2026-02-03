from http import HTTPStatus

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

from fastapi.responses import JSONResponse
from sqlalchemy import select
from api import schemas
from api.cruds import (
    Event,
    Exhibition,
    PushToken,
)
from api.configuration.database.db_helper import db_helper
from api.models.associations import push_token_activity_type_association
from api.models.enum import AgeEnum, ActivityTypeEnum

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
        category_ids: List[int] = Query(None, description="Category"),
        age: List[AgeEnum] = Query(None, description="Age"),
        disabilities: bool = Query(None, description="Disabilities"),
        is_free: bool = Query(None, description="Is free"),
        privilege_ticket: bool = Query(None, description="Privilege ticket"),
        pushkin_card: bool = Query(None, description="Pay by pushkin card"),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    events, total_count = await Event.filter(
        session,
        genre_ids,
        location_ids,
        category_ids,
        age,
        disabilities,
        is_free,
        privilege_ticket,
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
        location: List[int] = Query(None, description="Location"),
        category: List[int] = Query(None, description="Category"),
        age: List[AgeEnum] = Query(None, description="Age"),
        disabilities: bool = Query(None, description="Disabilities"),
        is_free: bool = Query(None, description="Is free"),
        privilege_ticket: bool = Query(None, description="Privilege ticket"),
        pushkin_card: bool = Query(None, description="Pay by pushkin card"),
        audio_guide: bool = Query(None, description="Has audio guide"),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    exhibitions, total_count = await Exhibition.filter(
        session,
        location,
        category,
        age,
        disabilities,
        is_free,
        privilege_ticket,
        pushkin_card,
        audio_guide,
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
    status_code=201,
    responses=response_codes,
)
async def create_preference(
        payload: schemas.ActivityPreferencesCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> JSONResponse:
    await PushToken.create_preference(
        session,
        payload.push_token,
        payload.tags,
        payload.activity_types,
        payload.genres,
        payload.ages,
    )
    return JSONResponse({"message": "created"}, HTTPStatus.CREATED)


@site_router.get(
    "/preferences",
    response_model=schemas.ActivityPreferencesGet,
    status_code=200,
    responses=response_codes,
)
async def get_preferences(
        push_token: str = Query(..., description="Push token string"),
        limit: int = Query(6, gt=0, le=10, description="Limit by each category"),
        offset: int = Query(0, ge=0, description="Limit by each category"),
        need_more: bool = Query(True, description="Need more cards"),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    push_token_obj = await PushToken.get_by_token(session, push_token)

    activity_result = await session.execute(
        select(push_token_activity_type_association.c.type)
        .where(push_token_activity_type_association.c.push_token_id == push_token_obj.id)
    )
    activity_types = [row[0] for row in activity_result.all()]

    if not activity_types or ActivityTypeEnum.EXHIBITION in activity_types:
        exhibitions = await Exhibition.get_by_preferences(session, push_token_obj)
    else:
        exhibitions = []

    if not activity_types or ActivityTypeEnum.EVENT in activity_types:
        events = await Event.get_by_preferences(session, push_token_obj)
    else:
        events = []

    all_cards = exhibitions + events
    total = len(all_cards)

    if need_more:
        exhibitions_chunk = exhibitions[:3]
        events_chunk = events[:3]
        chunk = exhibitions_chunk + events_chunk
    else:
        chunk = all_cards[offset:offset + limit]

    return schemas.ActivityPreferencesGet(items=chunk, total=total)
