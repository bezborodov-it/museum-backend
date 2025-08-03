from datetime import datetime, timezone, date
from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import declared_attr
import pytz


def now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class DateORMMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: now(),
        onupdate=lambda: now(),
        nullable=False,
    )

    @classmethod
    def now(cls) -> datetime:
        return now()

    @classmethod
    def date_now(cls) -> date:
        return now().date()
