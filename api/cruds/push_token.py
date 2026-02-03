from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, insert

from api.cruds.base import Base, with_model
from api.exceptions.cruds import NotFoundError
from api.models import PushTokenORM
from api.models.associations import push_token_activity_type_association, push_token_age_association
from api.models.enum import ActivityTypeEnum, AgeEnum


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
        if obj is None:
            raise NotFoundError(cls.model.__tablename__, "token", push_token)
        return obj

    @classmethod
    async def create_preference(
        cls,
        session: AsyncSession,
        push_token: str,
        tag_ids: List[int],
        activity_types: List[ActivityTypeEnum],
        genre_ids: List[int],
        ages: List[AgeEnum]
    ):

        push_token_obj = await cls.get_by_token(session, push_token)
        if push_token_obj is None:
            data = {"push_token": push_token}
            push_token_obj = await cls.create(session, data)

        data = {
            "tags": tag_ids,
            "genres": genre_ids
        }

        if data:
            push_token_obj = await cls.update(session, push_token_obj.id, data)

        if activity_types:
            await session.execute(
                delete(push_token_activity_type_association).where(
                    push_token_activity_type_association.c.push_token_id == push_token_obj.id
                )
            )

            # Добавляем новые связи
            for activity_type in activity_types:
                await session.execute(
                    insert(push_token_activity_type_association).values(
                        push_token_id=push_token_obj.id,
                        type=activity_type
                    )
                )

            # Обработка ages через association таблицу
        if ages:
            # Удаляем старые связи
            await session.execute(
                delete(push_token_age_association).where(
                    push_token_age_association.c.push_token_id == push_token_obj.id
                )
            )

            # Добавляем новые связи
            for age in ages:
                await session.execute(
                    insert(push_token_age_association).values(
                        push_token_id=push_token_obj.id,
                        age=age
                    )
                )

        await session.commit()
        await session.refresh(push_token_obj)
