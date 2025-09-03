from typing import Optional, Dict, Any, List
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone

from api.utils.base import str_ekb_to_utc


class PushTokenBase(BaseModel):
    id: int
    push_token: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PushTokenCreate(BaseModel):
    push_token: str


class NotificationBase(BaseModel):
    id: int
    title: str
    body: str
    time_to_send: datetime

    class Config:
        from_attributes = True

class NotificationsAdminGet(BaseModel):
    items: List[NotificationBase]
    total: int


class NotificationsGet(BaseModel):
    items: List[NotificationBase]
    total: int


class NotificationCreate(BaseModel):
    title: str
    body: str
    time_to_send: datetime

    @field_validator("time_to_send", mode="before")
    @classmethod
    def convert_and_validate(cls, value: str) -> datetime:
        dt_utc = str_ekb_to_utc(value)
        now_utc = datetime.now(timezone.utc)

        if dt_utc < now_utc:
            raise ValueError("Время отправки должно быть в будущем")

        return dt_utc