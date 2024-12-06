from typing import Optional, List
from fastapi import Form
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
        from_attributes = True


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
    notification_type: Optional[str]
    operation_id: Optional[str]
    amount: Optional[float]
    withdraw_amount: Optional[float]
    currency: Optional[str]
    datetime: Optional[datetime]
    sender: Optional[str]
    codepro: Optional[bool]
    label: Optional[str]
    sha1_hash: Optional[str]
    unaccepted: Optional[bool]

    @classmethod
    def as_form(
            cls,
            notification_type: Optional[str] = Form(None),
            operation_id: Optional[str] = Form(None),
            amount: Optional[float] = Form(None),
            withdraw_amount: Optional[float] = Form(None),
            currency: Optional[str] = Form(None),
            datetime: Optional[datetime] = Form(None),
            sender: Optional[str] = Form(None),
            codepro: Optional[bool] = Form(None),
            label: Optional[str] = Form(None),
            sha1_hash: Optional[str] = Form(None),
            unaccepted: Optional[bool] = Form(None),
    ) -> "PaymentCallback":
        return cls(
            notification_type=notification_type,
            operation_id=operation_id,
            amount=amount,
            withdraw_amount=withdraw_amount,
            currency=currency,
            datetime=datetime,
            sender=sender,
            codepro=codepro,
            label=label,
            sha1_hash=sha1_hash,
            unaccepted=unaccepted,
        )


class ShallowTicket(BaseModel):
    id: int
    type: TicketTypeEnum
    price: int
    event_date: datetime

    class Config:
        from_attributes = True
