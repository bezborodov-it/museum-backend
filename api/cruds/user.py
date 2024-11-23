from datetime import datetime
from sqlalchemy import select, delete, func
from typing import Dict, Any, List
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import UserORM, TicketORM
from api.models.associations import (
    user_tag_preference_association,
    user_genre_preference_association,
)
from api.models.enums import FilterTicketTypeEnum, FilterTicketStatusEnum


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

    @classmethod
    async def filter_tickets(
        cls,
        session: AsyncSession,
        user_id: int,
        ticket_status: List[FilterTicketStatusEnum] = None,
        ticket_type: List[FilterTicketTypeEnum] = None,
        offset: int = 0,
        limit: int = 10,
    ) -> List[TicketORM]:
        query = select(TicketORM).where(TicketORM.customer_id == user_id)

        if ticket_status:
            query = query.where(TicketORM.status.in_(ticket_status))

        if ticket_type:
            query = query.where(TicketORM.type.in_(ticket_type))

        total_count = await session.scalar(
            select(func.count()).select_from(query.subquery())
        )

        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all(), total_count
