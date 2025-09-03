from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.models import UserORM


@with_model(UserORM)
class User(Base):
    @classmethod
    async def get_by_login(cls, session: AsyncSession, login: str) -> UserORM:
        query = select(UserORM).where(cls.model.login == login)
        result = await session.execute(query)
        return result.scalars().first()
