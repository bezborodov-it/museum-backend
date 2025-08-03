from http.client import HTTPResponse

from fastapi import (
    APIRouter,
    Depends,
    Response,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api import schemas
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user, get_basic_user
from api.models import UserORM
from api.cruds import PushToken
from api.service import expo_push_notification
from api.service.celery import send_mass_push
from fastapi.responses import JSONResponse

site_router = APIRouter(prefix="/notification", tags=["notification"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.post("/push_token", response_model=schemas.PushTokenBase)
async def save_push_token(
        payload: schemas.PushTokenCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_current_user),
) -> Response:
    existing_token = await PushToken.get_by_user_id(session, current_user.id)
    if not existing_token:
        data = {'user_id': current_user.id, 'expo_push_token': payload.expo_push_token}
        push_token = await PushToken.create(session, data)
        return push_token

    if existing_token.expo_push_token != payload.expo_push_token:
        data = {'expo_push_token': payload.expo_push_token, 'is_active': True}
        push_token = await PushToken.update(session, existing_token.id, data)
        return push_token

    return existing_token


@site_router.post("/mass-message", tags=["admin"], status_code=202)
async def send_mass_message(
        payload: schemas.NotificationCreate,
        session: AsyncSession = Depends(db_helper.session_getter),
        current_user: UserORM = Depends(get_basic_user),
) -> Response:
    try:

        kwargs = {
            "title": payload.title,
            "body": payload.body,
            "data": payload.data,
        }
        send_mass_push.apply_async(
            kwargs=kwargs,
            eta=payload.time_to_send
        )
        return JSONResponse(status_code=202, content={"detail": "Push-уведомление запланировано"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
