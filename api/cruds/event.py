from sqlalchemy import select, or_, func, case
from typing import List, Tuple

from api.models.enums import FilterVisitorCategoryEnum, FilterEventGenreEnum
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import (
    EventORM,
    VisitorCategoryORM,
    EventGenreORM,
    LocationORM,
    UserORM,
    EventTagORM,
    TicketORM,
)
from api.exceptions.cruds import ModelNotFoundError
from api import schemas
from api.models.enums import TicketStatusEnum
from api.models.associations import event_visitor_category_association


@with_model(EventORM)
class Event(Base):

    @classmethod
    async def update_image_url(
            cls, session: AsyncSession, event_id: int, image_url: str
    ) -> EventORM:
        event = await cls.get_by_id(session, event_id)
        event.image_url = image_url
        await session.commit()
        await session.refresh(event)
        return event

    @classmethod
    async def filter(
            cls,
            session: AsyncSession,
            genre: List[int] = None,
            location: List[int] = None,
            visitor_category: List[int] = None,
            disabilities: bool = None,
            offset: int = 0,
            limit: int = 10,
    ) -> List[EventORM]:
        query = select(
            EventORM,
            func.min(TicketORM.price).label("min_price"),
            func.min(TicketORM.event_date).label("nearest_date"),
        ).join(TicketORM, TicketORM.event_id == EventORM.id, isouter=True)

        if genre:
            query = query.filter(EventORM.genre_id.in_(genre))

        if location is not None:
            query = query.filter(EventORM.location_id.in_(location))

        if visitor_category:
            query = query.join(event_visitor_category_association).filter(
                event_visitor_category_association.c.visitor_category_id.in_(
                    visitor_category
                )
            )

        if disabilities is not None:
            query = query.filter(EventORM.disabilities == disabilities)

        query = query.group_by(EventORM.id)
        query = query.order_by(func.min(TicketORM.event_date))

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        events = [
            {**event[0].__dict__, "min_price": event[1], "nearest_date": event[2]}
            for event in result.fetchall()
        ]

        return events, total_count

    @classmethod
    async def get_events_by_user_preferences(
            cls,
            session: AsyncSession,
            current_user: UserORM,
            offset: int = 0,
            limit: int = 10,
    ) -> List[EventORM]:
        user_tag_ids = [tag.id for tag in current_user.tags]
        user_genre_ids = [genre.id for genre in current_user.genres]

        query = (
            select(EventORM)
            .join(EventORM.tag, isouter=True)
            .join(EventORM.genre, isouter=True)
            .filter(
                or_(
                    EventTagORM.id.in_(user_tag_ids),
                    EventGenreORM.id.in_(user_genre_ids),
                )
            )
            .distinct()
        )

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all(), total_count

    @classmethod
    async def get_admin(
            cls,
            session: AsyncSession,
            offset: int = 0,
            limit: int = 10,
    ) -> List[EventORM]:
        query = select(cls.model)

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)

        events = result.scalars().all()

        return events, total_count

    @classmethod
    async def get_admin_event_by_id(
            cls, session: AsyncSession, event_id: int
    ) -> Tuple[EventORM, int, int, int]:
        query = (
            select(
                cls.model,
                func.count(
                    case((TicketORM.status == TicketStatusEnum.available, 1))
                ).label("ticket_available"),
                func.count(
                    case((TicketORM.status == TicketStatusEnum.booked, 1))
                ).label("ticket_booked"),
                func.count(
                    case((TicketORM.status == TicketStatusEnum.sold, 1))
                ).label("ticket_sold"),
            )
            .join(TicketORM, TicketORM.event_id == cls.model.id, isouter=True)
            .where(cls.model.id == event_id)
            .group_by(cls.model.id)
        )

        result = await session.execute(query)
        row = result.one_or_none()
        if row is None:
            raise ModelNotFoundError(cls.model.__tablename__, "id", event_id)

        return row
