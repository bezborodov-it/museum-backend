from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    Path,
    UploadFile,
    Query,
)
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from api import schemas
from api.cruds import Ticket
from api.configuration.database.db_helper import db_helper
from api.dependencies import get_current_user, is_admin, get_image_with
from api.models import UserORM
from api.models.enums import FilterEventGenreEnum, FilterVisitorCategoryEnum
from api.utils.image import save_event_image
from api.service.redis import redis_service
from api.service.celery import (
    ticket_revert_transaction_without_payment,
    ticket_revert_booked_without_transaction,
)

site_router = APIRouter(prefix="/ticket", tags=["ticket"])

response_codes = {
    200: {"description": "Success"},
    404: {"description": "Not found", "model": schemas.ErrorNotFound},
    500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
}


@site_router.post(
    "",
    response_model=List[schemas.TicketBase],
    status_code=201,
    responses={
        201: {"description": "Success"},
        400: {"description": "Bad Request", "model": schemas.ErrorGeneral},
        404: {"description": "Not found", "model": schemas.ErrorNotFound},
        500: {"description": "Internal server error", "model": schemas.ErrorGeneral},
    },
)
async def create_tickets(
    payload: schemas.TicketCreate,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(is_admin),
) -> Response:
    tickets = await Ticket.create_bulk(session, payload.dict())
    return tickets


@site_router.post("/book/{ticket_id}", response_model=schemas.TicketBase)
async def book_ticket(
    ticket_id: PositiveInt,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    booked_ticket = await Ticket.book(session, ticket_id, current_user.id)
    return booked_ticket


@site_router.post("/purchase/{ticket_id}", response_model=schemas.TicketPurchase)
async def purchase_ticket(
    ticket_id: PositiveInt,
    session: AsyncSession = Depends(db_helper.session_getter),
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    url = await Ticket.create_purchase_url(session, ticket_id, current_user.id)
    await redis_service.redis.set(ticket_id, url, ex=900)
    ticket_revert_transaction_without_payment.apply_async((ticket_id,), countdown=910)
    return schemas.TicketPurchase(url=url)


@site_router.post("/purchase/{ticket_id}/url", response_model=schemas.TicketPurchase)
async def get_temporary_purchase_url(
    ticket_id: PositiveInt,
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    stored_url = await redis_service.redis.get(ticket_id)
    if stored_url is None:
        raise HTTPException(status_code=400, detail="Payment ticket time is expired")
    return schemas.TicketPurchase(url=stored_url)


@site_router.post("/payment/callback", response_model=schemas.TicketBase)
async def payment_callback(
    payload: schemas.PaymentCallback,
    session: AsyncSession = Depends(db_helper.session_getter),
) -> Response:
    sold_ticket = await Ticket.update_after_success_purchase(session, payload.dict())
    await redis_service.redis.delete(ticket_id)
    return sold_ticket


@site_router.get(
    "/{ticket_id}",
    response_model=schemas.TicketBase,
    status_code=200,
    responses=response_codes,
)
async def get_ticket_by_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    ticket_id: PositiveInt = Path(..., description="The identifier of ticket"),
    current_user: UserORM = Depends(get_current_user),
) -> Response:
    ticket = await Ticket.get_by_id(session, ticket_id)
    return ticket


@site_router.get(
    "/avaliable/{event_id}",
    response_model=List[schemas.ShallowTicket],
    status_code=200,
    responses=response_codes,
)
async def get_avaliable_tickets_by_event_id(
    session: AsyncSession = Depends(db_helper.session_getter),
    event_id: PositiveInt = Path(..., description="The identifier of event"),
) -> Response:
    avaliable_tickets = await Ticket.get_avaliable_event(session, event_id)
    return avaliable_tickets
