from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from api.cruds.base import Base, with_model
from api.exceptions.cruds import NotFoundError
from api.models import PushTokenORM


@with_model(PushTokenORM)
class PushToken(Base):

    @classmethod
    async def get_by_token(
        cls,
        session: AsyncSession,
        push_token: str,
    ) -> PushTokenORM:
        query = select(cls.model).where(cls.model.push_token == push_token)
        result = await session.execute(query)
        obj = result.scalar_one_or_none()
        return obj

    @classmethod
    async def create_preference(
        cls,
        session: AsyncSession,
        push_token: str,
        tag_ids: List[int],
        genre_ids: List[int],
    ) -> PushTokenORM:

        push_token_obj = await cls.get_by_token(session, push_token)
        if push_token_obj is None:
            data = {"push_token": push_token}
            push_token_obj = await cls.create(session, data)

        data = {
            "tags": tag_ids,
            "genres": genre_ids,
        }

        if data:
            push_token_obj = await cls.update(session, push_token_obj.id, data)

        return push_token_obj
