from fastapi import APIRouter, Depends, Response, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from api import schemas
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_basic_user
from api.models import UserORM
from api.cruds import PushToken, Notification
from api.celery.tasks import send_mass_push
from fastapi.responses import JSONResponse

site_router = APIRouter(prefix="/notification", tags=["notification"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.post(
    "/push_token",
    response_model=schemas.PushTokenBase,
    responses=response_codes,
)
async def save_push_token(
        payload: schemas.PushTokenCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    token = await PushToken.get_by_token(session, payload.push_token)
    if token:
        raise HTTPException(status_code=400, detail="Token already exists")
    data = {"push_token": payload.push_token}
    push_token = await PushToken.create(session, data)
    return push_token


@site_router.get(
    "s",
    tags=["admin"],
    response_model=schemas.NotificationsAdminGet
)
async def get_notifications(
        search: Optional[str] = Query(None, description="Search string"),
        offset: int = Query(0, ge=0, description="Offset"),
        limit: int = Query(10, gt=0, le=100, description="Limit"),
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    notifications, total_count = await Notification.get_admin_list(session, search, offset, limit, True)
    return schemas.NotificationsAdminGet(items=notifications, total=total_count)


@site_router.post("/mass-message", tags=["admin"], status_code=202)
async def send_mass_message(
        payload: schemas.NotificationCreate,
        current_user: UserORM = Depends(get_basic_user),
        session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    try:
        notification = await Notification.create(session, payload.model_dump())
        push_tokens = await PushToken.get_all(session)
        tokens = [
            token.push_token for token in push_tokens
        ]
        send_mass_push.apply_async(
            args=[notification.id, tokens, payload.title, payload.body],
            eta=payload.time_to_send,
        )
        return JSONResponse(
            status_code=202, content={"detail": "Push-уведомление запланировано"}
        )
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
