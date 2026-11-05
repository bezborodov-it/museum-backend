from sqlalchemy import select, func, case, cast, String, and_, or_
from typing import List
from datetime import datetime, timedelta
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    EventORM,
    PushTokenORM,
    TagORM,
    GenreORM,
)
from api.models.associations import push_token_age_association
from api.models.enum import AgeEnum, ActivityVisibilityEnum
from api.utils.age import build_age_priority_and_allowed


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
            category_ids: List[int] = None,
            age: List[AgeEnum] = None,
            disabilities: bool = None,
            is_free: bool = None,
            privilege_ticket: bool = None,
            pushkin_card: bool = None,
            offset: int = 0,
            limit: int = 10,
    ) -> List[EventORM]:
        query = select(cls.model)
        query = query.filter(
            cls.model.date_start >= datetime.now() + timedelta(hours=5),
            cls.model.status == ActivityVisibilityEnum.ACTIVE,
        )

        if genre_ids:
            query = query.filter(cls.model.genre_id.in_(genre_ids))

        if location_ids:
            has_null = -1 in location_ids
            real_ids = [x for x in location_ids if x != -1]

            if has_null and real_ids:
                query = query.filter(or_(
                    cls.model.location_id.in_(real_ids),
                    cls.model.location_id.is_(None),
                ))
            elif has_null:
                query = query.filter(cls.model.location_id.is_(None))
            else:
                query = query.filter(cls.model.location_id.in_(real_ids))

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

        events = result.scalars().unique().all()
        return events, total_count

    @classmethod
    async def get_by_preferences(
            cls, session: AsyncSession, push_token_obj: PushTokenORM
    ) -> List[EventORM]:

        genres = (
            [g.id for g in push_token_obj.genres] if push_token_obj.genres else None
        )
        tags = [t.id for t in push_token_obj.tags] if push_token_obj.tags else None
        ages_result = await session.execute(
            select(push_token_age_association.c.age)
            .where(push_token_age_association.c.push_token_id == push_token_obj.id)
        )
        ages = [AgeEnum(a) for a in ages_result.scalars().all()]

        query = select(cls.model)
        query = query.filter(
            cls.model.date_start >= datetime.now() + timedelta(hours=5),
            cls.model.status == ActivityVisibilityEnum.ACTIVE,
        )

        if tags:
            query = query.join(cls.model.tags).filter(TagORM.id.in_(tags))

        if genres:
            query = query.join(cls.model.genre).filter(GenreORM.id.in_(genres))

        if ages:
            age_priority, allowed_ages = build_age_priority_and_allowed(cls.model.age, ages)
            query = query.filter(cls.model.age.in_(allowed_ages))
            query = query.order_by(
                cls.model.date_start.asc(),
                age_priority.asc()
            )

        else:
            query = query.order_by(
                cls.model.date_start.asc()
            )

        result = await session.execute(query)
        events = result.scalars().unique().all()
        return events

    from sqlalchemy import case, func, and_

    @classmethod
    async def get_admin_list(
            cls,
            session: AsyncSession,
            search: str,
            status: ActivityVisibilityEnum | None = None,
            offset: int = 0,
            limit: int = 10,
            is_notification: bool = False,
    ):
        now = func.now()

        query = select(cls.model)

        if search:
            field = cls.model.title if is_notification else cls.model.name
            query = query.where(field.ilike(f"%{search}%"))

        if status is not None:
            query = query.where(cls.model.status == status)

        query = query.order_by(
            case(
                (cls.model.date_start >= now, 0),
                else_=1,
            ),
            case(
                (cls.model.date_start >= now, cls.model.date_start),
                else_=None,
            ).asc(),
            cls.model.date_start.desc(),
            cls.model.id.desc(),
        )

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        items = result.scalars().all()

        return items, total_count