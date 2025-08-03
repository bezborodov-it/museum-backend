from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.models import PushTokenORM


@with_model(PushTokenORM)
class PushToken(Base):

    @classmethod
    async def get_by_user_id(cls, session: AsyncSession, user_id: int) -> PushTokenORM:
       query = select(PushTokenORM).where(PushTokenORM.user_id == user_id)
       result = await session.execute(query)
       return result.scalars().first()

    @classmethod
    async def get_active(cls, session: AsyncSession) -> Sequence[PushTokenORM]:
        query = select(PushTokenORM).where(PushTokenORM.is_active == True)
        result = await session.execute(query)
        return result.scalars().all()


