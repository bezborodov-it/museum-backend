from sqlalchemy import select, func, or_
from typing import List

from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    EventORM,
    VisitorCategoryORM,
    PushTokenORM,
    TagORM,
    GenreORM,
)


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def update_image_url(
        cls, session: AsyncSession, event_id: int, image_url: str
    ) -> EventORM:
        event = await cls.update(session, event_id, {"image_url": image_url})
        return event

    @classmethod
    async def filter(
        cls,
        session: AsyncSession,
        genre_ids: List[int] = None,
        location_ids: List[int] = None,
        visitor_category_ids: List[int] = None,
        category_ids: List[int] = None,
        disabilities: bool = None,
        is_free: bool = None,
        pushkin_card: bool = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[EventORM]:
        query = select(cls.model)

        if genre_ids:
            query = query.filter(cls.model.genre_id.in_(genre_ids))

        if location_ids:
            query = query.filter(cls.model.location_id.in_(location_ids))

        if visitor_category_ids:
            query = query.filter(cls.model.location_id.in_(visitor_category_ids))

        if category_ids:
            query = query.filter(cls.model.category_id.in_(category_ids))

        if disabilities is not None:
            query = query.filter(cls.model.disabilities == disabilities)

        if is_free is not None:
            query = query.filter(cls.model.is_free == is_free)

        if pushkin_card is not None:
            query = query.filter(cls.model.pushkin_card == pushkin_card)

        query = query.group_by(cls.model.id)
        query = query.order_by(
            cls.model.pinned_order.is_(None),
            cls.model.pinned_order.asc(),
            func.min(cls.model.date_start).asc(),
        )

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        events = result.scalars().unique().all()
        return events, total_count

    @classmethod
    async def get_by_preferences(
        cls, session: AsyncSession, push_token_obj: PushTokenORM, limit: int = 3
    ) -> List[EventORM]:

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
        events = result.scalars().unique().all()
        return events
