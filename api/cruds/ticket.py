from datetime import datetime

from sqlalchemy import select, or_
from typing import List, Dict, Any
from datetime import timezone

from api import schemas
from api.models.enums import FilterVisitorCategoryEnum, FilterEventGenreEnum
from api.cruds.base import Base, with_model
from sqlalchemy.ext.asyncio import AsyncSession
from api.models import TicketORM
from api.models.enums import TicketStatusEnum
from api.exceptions.base import TicketNotAvailableError
from api.service.yoomoney import yoomoney
from api.utils.qr_code import generate_qr_code_base64


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
    async def get_avaliable_event(
        cls, session: AsyncSession, event_id: int
    ) -> List[TicketORM]:
        query = select(TicketORM).filter(
            TicketORM.event_id == event_id,
            TicketORM.status == TicketStatusEnum.available,
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def create_purchase_url(
        cls,
        session: AsyncSession,
        ticket_id: int,
        user_id: int,
    ) -> schemas.TicketPurchase:
        ticket = await cls.get_by_id(session, ticket_id)
        if (
            ticket.status == TicketStatusEnum.sold
            or ticket.status == TicketStatusEnum.transaction
        ):
            raise TicketNotAvailableError("Ticket is not available for purchase.")

        if ticket.customer_id is not None and ticket.customer_id != user_id:
            raise TicketNotAvailableError(
                "Ticket is not available for purchase. It's booked by another user"
            )

        purchase_url, label = yoomoney.create_payment_url(
            amount=ticket.price,
        )

        await Ticket.update(
            session,
            ticket_id,
            {
                "customer_id": user_id,
                "status": TicketStatusEnum.transaction,
                "transaction_label": label,
            },
        )

        return purchase_url

    @classmethod
    async def get_by_transaction_label(
        cls, session: AsyncSession, label: str
    ) -> TicketORM:
        query = select(TicketORM).where(TicketORM.transaction_label == label)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def update_after_success_purchase(
        cls, session: AsyncSession, data: Dict
    ) -> TicketORM:
        valid_hash = yoomoney.verify_payment(data)
        if valid_hash:
            ticket = await cls.get_by_transaction_label(session, data["label"])
            if not ticket:
                raise TicketNotAvailableError("Not found ticket with this label")
            if ticket.status == TicketStatusEnum.sold:
                raise TicketNotAvailableError("Ticket is already sold.")

            qr_data = f"TicketID:{ticket.id}|Event:{ticket.event.id}|Date:{ticket.event_date}|Price:{ticket.price}"
            qr_code = generate_qr_code_base64(qr_data)

            datetime_without_tz = (
                data["datetime"].astimezone(timezone.utc).replace(tzinfo=None)
            )

            await Ticket.update(
                session,
                ticket.id,
                {
                    "status": TicketStatusEnum.sold,
                    "purchased_at": datetime_without_tz,
                    "qr_code": qr_code,
                },
            )
            return ticket

    @classmethod
    async def get_booked_all(cls, session: AsyncSession) -> List[TicketORM]:
        query = select(TicketORM).filter(
            TicketORM.status == TicketStatusEnum.booked,
        )
        result = await session.execute(query)
        return result.scalars().all()
