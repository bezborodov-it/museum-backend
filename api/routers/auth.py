from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime, UTC

from api.configuration.config import settings
from api import schemas
from api.cruds import User, RefreshToken
from api.configuration.database.db_helper import db_helper
from api.utils.auth import (
    generate_verification_code,
    create_access_token,
    create_refresh_token,
)
from api.service.redis import redis_service
from api.service.whatsapp import whatsapp_bot

site_router = APIRouter(prefix="/auth", tags=["auth"])


@site_router.post(
    "/send_code",
    response_model=schemas.VerificationCodeGet,
    status_code=200,
    responses={
        200: {"description": "Success"},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def send_code(
    payload: schemas.PhoneNumberGet,
) -> Response:
    verification_code = await generate_verification_code()
    await redis_service.redis.set(payload.number, verification_code, ex=300)

    message = settings.AUTH_MESSAGE_TEMPLATE.format(verification_code=verification_code)
    response = await whatsapp_bot.send_message(payload.number, message)

    if not response.get("idMessage"):
        raise HTTPException(status_code=400, detail="Failed to send verification code")

    return {"code": verification_code}


@site_router.post(
    "/login",
    response_model=schemas.TokensResponse,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {
            "description": "Invalid verification code",
            "model": schemas.ErrorGeneral,
        },
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def verify_code(
    payload: schemas.LoginRequestGet,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    stored_code = await redis_service.redis.get(payload.number)
    if stored_code is None or stored_code != payload.code:
        raise HTTPException(status_code=400, detail="Invalid verification code")

    await redis_service.redis.delete(payload.number)

    user = await User.get_user_by_phone(session, payload.number)
    if not user:
        user = await User.create(session, {"number": payload.number})

    access = create_access_token(user)
    refresh, expire_at = create_refresh_token(user)

    await RefreshToken.create(
        session, {"user": user, "token": refresh, "expires": expire_at}
    )

    return {"access_token": access, "refresh_token": refresh}


@site_router.post(
    "/refresh",
    response_model=schemas.RefreshTokenResponse,
    status_code=200,
    responses={
        200: {"description": "Success"},
        400: {
            "description": "Invalid or expired refresh token",
            "model": schemas.ErrorGeneral,
        },
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def refresh_token(
    payload: schemas.RefreshTokenGet,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    stored_token = await RefreshToken.get_by_token(session, payload.refresh_token)

    if not stored_token or stored_token.expires < datetime.now(UTC):
        raise HTTPException(status_code=400, detail="Invalid refresh token")

    user = await User.get_by_id(session, stored_token.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    return {"access_token": create_access_token(user)}
