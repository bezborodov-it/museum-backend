from sqlalchemy import select, delete
from typing import Dict, Any
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import UserORM
from api.models.associations import user_tag_preference_association, user_genre_preference_association


@with_model(UserORM)
class User(Base):
    @classmethod
    async def get_user_by_email(cls, session: AsyncSession, email: str):
        query = select(UserORM).where(UserORM.email == email)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def get_user_by_phone(
            cls, session: AsyncSession, phone_number: str
    ) -> UserORM:
        query = select(UserORM).where(UserORM.number == phone_number)
        result = await session.execute(query)
        return result.scalars().first()
