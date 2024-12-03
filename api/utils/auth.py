import random
import string
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Tuple, Dict
from datetime import datetime, timezone

from api.configuration.config import settings
from api.models.orms import UserORM


async def generate_verification_code() -> str:
    return "".join(random.choices(string.digits, k=6))


def generate_jwt_token(data: Dict[str, any], expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def create_access_token(user: UserORM) -> str:
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    access_token = generate_jwt_token(
        data={"sub": user.number}, expires_delta=access_token_expires
    )

    return access_token


def create_refresh_token(user: UserORM) -> str:
    refresh_token_expires = timedelta(days=int(settings.REFRESH_TOKEN_EXPIRE_DAYS))
    expire_at = datetime.now(timezone.utc) + refresh_token_expires

    refresh_token = generate_jwt_token(
        data={"sub": user.number}, expires_delta=refresh_token_expires
    )

    return refresh_token, expire_at


def decode_access_token(token: str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None
