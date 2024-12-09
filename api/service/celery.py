import os
import time
from celery import Celery
import asyncio
from celery.schedules import crontab
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync

from api.configuration.database.db_helper import db_helper
from api.configuration.config import settings
from api.cruds import Ticket
from api.models.enums import TicketStatusEnum

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL",
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)
celery.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND",
    f"redis://:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
)
celery.conf.beat_schedule = {
    "ticket_revert_booked_check": {
        "task": "ticket_revert_booked_without_transaction",
        "schedule": crontab(minute=0, hour="*/6")  # Каждые 6 часов
    },
}


@celery.task(name="ticket_revert_transaction_without_payment")
def ticket_revert_transaction_without_payment(ticket_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(process_ticket_revert(ticket_id))


async def process_ticket_revert(ticket_id: int):
    try:
        async for session in db_helper.session_getter():
            ticket = await Ticket.get_by_id(session, ticket_id)
            print(ticket)
            if ticket.status == TicketStatusEnum.transaction:
                await Ticket.update(
                    session,
                    ticket_id,
                    {
                        "customer_id": None,
                        "status": TicketStatusEnum.available,
                        "transaction_label": None,
                    },
                )
                print(f"Ticket {ticket_id} returned to available status.")
    except Exception as e:
        print(f"Error in task ticket_revert_transaction_without_payment: {e}")


@celery.task(name="ticket_revert_booked_without_transaction")
def ticket_revert_booked_without_transaction():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(process_revert_booked_without_transaction())
    return result


async def process_revert_booked_without_transaction():
    try:
        async for session in db_helper.session_getter():
            tickets = await Ticket.get_booked_all(session)

            updated_tickets = []
            for ticket in tickets:
                time_left = ticket.event_date - datetime.now()

                if time_left <= timedelta(hours=48):
                    await Ticket.update(
                        session,
                        ticket.id,
                        {
                            "customer_id": None,
                            "status": TicketStatusEnum.available,
                            "booked_at": None,
                        },
                    )
                    updated_tickets.append(ticket.id)
                    print(f"Ticket {ticket.id} returned to available status.")
            return {"updated_tickets": updated_tickets}
    except Exception as e:
        print(f"Error in task ticket_revert_booked_without_transaction: {e}")
        return {"error": str(e)}
