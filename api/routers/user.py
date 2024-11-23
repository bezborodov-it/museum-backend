from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession

from api import schemas
from api.cruds import User
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user
from api.models import UserORM
from api.models.enums import FilterTicketStatusEnum, FilterTicketTypeEnum

from datetime import datetime

site_router = APIRouter(prefix="/user", tags=["user"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.get(
    "/me",
    response_model=schemas.UserBase,
    status_code=200,
    responses={
        200: {"description": "Success"},
    },
)
async def get_current_user(
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    return current_user


@site_router.put(
    "",
    response_model=schemas.UserBase,
    status_code=200,
    responses=response_codes,
)
async def update_current_user(
    pyload: schemas.UserUpdate,
    current_user: UserORM = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    user_data = pyload.dict(exclude_unset=True)
    updated_user = await User.update(session, current_user.id, user_data)

    return updated_user


@site_router.get(
    "/tickets/all",
    response_model=schemas.TicketFilterGet,
    status_code=200,
    responses=response_codes,
)
async def get_user_tickets(
    ticket_status: List[FilterTicketStatusEnum] = Query(
        None, description="Статус билета"
    ),
    ticket_type: List[FilterTicketTypeEnum] = Query(None, description="Тип билета"),
    offset: int = Query(0, ge=0, description="Offset"),
    limit: int = Query(10, gt=0, le=100, description="Limit"),
    current_user: UserORM = Depends(get_current_user),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    user_tickets, total_count = await User.filter_tickets(
        session, current_user.id, ticket_status, ticket_type, offset, limit
    )
    return {
        "items": user_tickets,
        "total": total_count,
    }
