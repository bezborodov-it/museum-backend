from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.cruds import User
from api.models import UserORM
from api.configuration.database.db_helper import db_helper
from api.utils.auth import verify_password


security = HTTPBasic()


async def get_basic_user(
    credentials: HTTPBasicCredentials = Depends(security),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> UserORM:
    user = await User.get_by_login(session, credentials.username)

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user
