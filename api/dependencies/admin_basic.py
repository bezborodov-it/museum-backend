from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.cruds import User
from api.models import UserORM
from api.models.enums import UserRoleEnum
from api.configuration.database.db_helper import db_helper
from api.utils.auth import verify_password


security = HTTPBasic()


async def get_basic_user(
        credentials: HTTPBasicCredentials = Depends(security),
        session: AsyncSession = Depends(db_helper.session_getter)
) -> UserORM:
    user = await User.get_user_by_phone(session, credentials.username)

    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    if UserRoleEnum.admin not in [role.role for role in user.roles]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    return user
