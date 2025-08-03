from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, field_validator
import pytz


class PushTokenBase(BaseModel):
    id: int
    expo_push_token: str
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime]

    class Config:
        from_attributes = True


class PushTokenCreate(BaseModel):
    expo_push_token: str

class NotificationCreate(BaseModel):
    title: str
    body: str
    time_to_send: datetime
    data: Optional[Dict[str, Any]] = None

    @field_validator('time_to_send', mode='before')
    @classmethod
    def parse_and_convert_to_utc(cls, value: str) -> datetime:

        parsed_time = datetime.fromisoformat(value)
        yekaterinburg_tz = pytz.timezone('Asia/Yekaterinburg')
        localized_time = yekaterinburg_tz.localize(parsed_time)

        return localized_time.astimezone(pytz.UTC)

    class Config:
        arbitrary_types_allowed = True