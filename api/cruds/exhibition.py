from sqlalchemy import select, or_, func, case
from typing import List, Tuple
from datetime import datetime, timedelta

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    PushTokenORM,
    GenreORM,
)
from api.models.associations import push_token_age_association
from api.models.enum import AgeEnum

from api.models.orms.event import ExhibitionORM, TagORM


@with_model(ExhibitionORM)
class Exhibition(Base):

    @classmethod
    async def update_image_url(
            cls, session: AsyncSession, exhibition_id: int, image_url: str
    ) -> ExhibitionORM:
        exhibition = await cls.update(session, exhibition_id, {"image_url": image_url})
        return exhibition

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            location_ids: List[int] = None,
            category_ids: List[int] = None,
            age: List[AgeEnum] = None,
            disabilities: bool = None,
            is_free: bool = None,
            privilege_ticket: bool = None,
            pushkin_card: bool = None,
            audio_guide: bool = None,
            offset: int = 0,
            limit: int = 10,
    ) -> List[ExhibitionORM]:
        query = select(cls.model)
        query = query.filter(cls.model.date_end >= datetime.now() + timedelta(hours=5))

        if location_ids:
            query = query.filter(cls.model.location_id.in_(location_ids))

        if category_ids:
            query = query.filter(cls.model.category_id.in_(category_ids))

        if age:
            age_values = [a.value for a in age]
            query = query.filter(cls.model.age.in_(age_values))

        if disabilities is not None:
            query = query.filter(cls.model.disabilities == disabilities)

        if is_free is not None:
            query = query.filter(cls.model.is_free == is_free)

        if pushkin_card is not None:
            query = query.filter(cls.model.pushkin_card == pushkin_card)

        if privilege_ticket is not None:
            query = query.filter(cls.model.privilege_ticket == privilege_ticket)

        if audio_guide is not None:
            query = query.filter(cls.model.audio_guide == audio_guide)

        query = query.group_by(cls.model.id)
        query = query.order_by(
            cls.model.pinned_order.is_(None),
            cls.model.pinned_order.asc(),
            func.min(cls.model.date_start).asc(),
            cls.model.id.asc(),
        )

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        exhibitions = result.scalars().unique().all()
        return exhibitions, total_count

    @classmethod
    async def get_by_preferences(
            cls, session: AsyncSession, push_token_obj: PushTokenORM
    ) -> List[ExhibitionORM]:

        tags = [t.id for t in push_token_obj.tags] if push_token_obj.tags else None
        ages_result = await session.execute(
            select(push_token_age_association.c.age)
            .where(push_token_age_association.c.push_token_id == push_token_obj.id)
        )
        ages = [row[0] for row in ages_result.all()] if ages_result else None

        query = select(cls.model)
        query = query.filter(cls.model.date_end >= datetime.now() + timedelta(hours=5))

        if tags:
            query = query.join(cls.model.tags).filter(TagORM.id.in_(tags))

        if ages:

            AGES_PRIORITY = [
                AgeEnum.EIGHTEEN_PLUS,
                AgeEnum.SIXTEEN_PLUS,
                AgeEnum.TWELVE_PLUS,
                AgeEnum.SIX_PLUS,
                AgeEnum.ZERO_PLUS,
            ]
            ordered = []
            for a in ages:
                if a in AGES_PRIORITY:
                    ordered.append(a)

            for a in AGES_PRIORITY:
                if a not in ordered:
                    ordered.append(a)

            age_order = case(
                {age: i for i, age in enumerate(ordered)},
                value=cls.model.age,
                else_=len(ordered),
            )

            query = query.order_by(cls.model.date_start.asc(), age_order.asc())
        else:
            query = query.order_by(cls.model.date_start.asc())

        query = query.group_by(cls.model.id)

        result = await session.execute(query)
        exhibitions = result.scalars().unique().all()
        return exhibitions
