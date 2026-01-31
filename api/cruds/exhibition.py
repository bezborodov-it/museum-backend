from sqlalchemy import select, or_, func, case
from typing import List, Tuple
from datetime import datetime, timedelta

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    VisitorCategoryORM,
    PushTokenORM,
    GenreORM,
)

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
        visitor_category_ids: List[int] = None,
        category_ids: List[int] = None,
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

        if visitor_category_ids:
            query = query.filter(
                cls.model.visitor_category_id.in_(visitor_category_ids)
            )

        if category_ids:
            query = query.filter(cls.model.category_id.in_(category_ids))

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
        cls, session: AsyncSession, push_token_obj: PushTokenORM, limit: int = 3
    ) -> List[ExhibitionORM]:

        genres = (
            [g.id for g in push_token_obj.genres] if push_token_obj.genres else None
        )
        visitor_categories = (
            [vc.id for vc in push_token_obj.visitor_categories]
            if push_token_obj.visitor_categories
            else None
        )
        tags = [t.id for t in push_token_obj.tags] if push_token_obj.tags else None

        query = select(cls.model)
        query = query.filter(cls.model.date_end >= datetime.now() + timedelta(hours=5))

        if tags:
            query = query.join(cls.model.tags).filter(TagORM.id.in_(tags))

        if visitor_categories:
            query = query.join(cls.model.visitor_category).filter(
                VisitorCategoryORM.id.in_(visitor_categories)
            )

        if genres:
            query = query.join(cls.model.genre).filter(GenreORM.id.in_(genres))

        query = query.group_by(cls.model.id)
        query = query.order_by(func.min(cls.model.date_start))
        query = query.limit(limit)

        result = await session.execute(query)
        exhibitions = result.scalars().unique().all()
        return exhibitions
