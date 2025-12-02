from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from api.cruds.base import Base, with_model
from api.models import AboutORM


@with_model(AboutORM)
class About(Base):

    @classmethod
    async def get_one(cls, session: AsyncSession) -> AboutORM:
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def update_one(cls, session: AsyncSession, data: Dict[str, Any]) -> AboutORM:
        about = await cls.get_one(session)
        updated_about = await cls.update(session, about.id, data)
        return updated_about
