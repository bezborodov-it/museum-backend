from typing import Optional, List
from datetime import datetime
from pydantic import validator, BaseModel, conint
from enum import Enum

from api.models.enums import TicketStatusEnum, TicketTypeEnum
from api.schemas import EventBase, UserBase, EventTicketGet


class TicketBase(BaseModel):
    id: int
    event: EventTicketGet
    status: TicketStatusEnum
    type: TicketTypeEnum
    price: int
    booked_at: Optional[datetime]
    purchased_at: Optional[datetime]
    event_date: datetime
    qr_code: Optional[str]

    class Config:
        orm_mode = True


class TicketCreate(BaseModel):
    event_id: int
    type: TicketTypeEnum
    price: int
    event_date: datetime
    quantity: conint(ge=1, le=100)


class TicketFilterGet(BaseModel):
    items: List[TicketBase]
    total: int


class TicketPurchase(BaseModel):
    url: str


class PaymentCallback(BaseModel):
    notification_type: str
    operation_id: str
    amount: float
    withdraw_amount: float
    currency: str
    datetime: datetime
    sender: str
    codepro: bool
    label: str
    sha1_hash: str
    unaccepted: bool


class ShallowTicket(BaseModel):
    id: int
    type: TicketTypeEnum
    price: int
    event_date: datetime

    class Config:
        orm_mode = True
