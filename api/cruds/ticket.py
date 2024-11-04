from datetime import datetime

from sqlalchemy import select, or_
from typing import List, Dict, Any

from api.models.enums import FilterVisitorCategoryEnum, FilterEventGenreEnum
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import TicketORM
from api.models.enums import TicketStatusEnum
from api.exceptions.base import TicketNotAvailableError


@with_model(TicketORM)
class Ticket(Base):

    @classmethod
    async def create_bulk(
        cls, session: AsyncSession, data: Dict[str, Any]
    ) -> List[TicketORM]:
        quantity = data.pop("quantity", 1)
        tickets = []

        for _ in range(quantity):
            ticket_data = data.copy()
            ticket = await cls.create(session, ticket_data)
            tickets.append(ticket)

        return tickets

    @classmethod
    async def book(
        cls, session: AsyncSession, ticket_id: int, user_id: int
    ) -> List[TicketORM]:
        ticket = await cls.get_by_id(session, ticket_id)

        if ticket.status != TicketStatusEnum.available:
            raise TicketNotAvailableError("Ticket is not available for reservation.")

        updated_data = {
            "customer_id": user_id,
            "status": TicketStatusEnum.booked,
            "booked_at": datetime.now(),
        }

        return await Ticket.update(session, ticket_id, updated_data)

    @classmethod
    async def get_avaliable(
        cls, session: AsyncSession, event_id: int
    ) -> List[TicketORM]:
        query = select(TicketORM).filter(
            TicketORM.event_id == event_id,
            TicketORM.status == TicketStatusEnum.available,
        )
        result = await session.execute(query)
        return result.scalars().all()
