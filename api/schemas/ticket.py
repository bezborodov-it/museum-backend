from typing import Optional, List
from datetime import datetime
from pydantic import validator, BaseModel
from enum import Enum

from api.models.enums import TicketStatusEnum, TicketTypeEnum
from api.schemas import EventBase, UserBase


class TicketBase(BaseModel):
    id: int
    event_id: int
    customer_id: Optional[int]
    status: TicketStatusEnum
    type: TicketTypeEnum
    price: int
    booked_at: Optional[datetime]
    purchased_at: Optional[datetime]
    event_date: datetime

    class Config:
        orm_mode = True


class TicketCreate(BaseModel):
    event_id: int
    type: TicketTypeEnum
    price: int
    event_date: datetime
    quantity: int
