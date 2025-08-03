import os
from celery import Celery
import asyncio

from celery.bin.result import result
from celery.schedules import crontab
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync

from api.configuration.database.db_helper import db_helper
from api.configuration.config import settings
from api.cruds import Ticket, PushToken, Notification
from api.models.enums import TicketStatusEnum, NotificationTypeEnum
from api.service import expo_push_notification
import json

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
celery.conf.timezone = "UTC"


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
        return None
    except Exception as e:
        print(f"Error in task ticket_revert_booked_without_transaction: {e}")
        return {"error": str(e)}

# Не работает пока что
@celery.task(name="send_mass_push")
def send_mass_push(title: str, body: str, data: dict = None):
    return asyncio.run(_send_push_to_active_users(title, body, data))


async def _send_push_to_active_users(title: str, body: str, data: dict = None):
    try:
        counter = 0
        async with db_helper.session_getter() as session:
            active_tokens = await PushToken.get_active(session)

        push_tokens = [active_token.expo_push_token for active_token in active_tokens]
        response_list = await expo_push_notification.send_mass_message(push_tokens, title, body, data)
        for batch_response, batch_tokens in zip(response_list,
                                                    [push_tokens[i:i + 100] for i in range(0, len(push_tokens), 100)]):
            data = batch_response.get("data", [])
            for i, res in enumerate(data):
                token = batch_tokens[i]

                push_token_obj = next((t for t in active_tokens if t.expo_push_token == token), None)
                if not push_token_obj:
                    continue

                if res.get("status") == "ok":
                    counter += 1
                async with db_helper.session_getter() as session:
                    if res.get("status") == "error" and res.get("details", {}).get("error") == "DeviceNotRegistered":
                        await PushToken.update(session, push_token_obj.id, {'is_active': False})

                    data = {
                        "push_token_id": push_token_obj.id,
                        "status": res.get("status"),
                        "result": json.dumps(res),
                        "type": NotificationTypeEnum.mass,
                    }
                    await Notification.create(session, data)

        return counter
    except Exception as e:
        return {"error": str(e)}
