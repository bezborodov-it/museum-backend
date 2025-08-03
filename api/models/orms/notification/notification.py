from sqlalchemy import (
    BigInteger,
    Column,
    String,
    DateTime,
    Boolean, Integer,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from api.models import DateORMMixin
from api.models.orms.base import BaseORM

class NotificationORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    is_sent = Column(Boolean, nullable=False, default=False)
    received = Column(Integer, nullable=False, default=0)
    time_to_send = Column(DateTime, nullable=False)
    data = Column(JSONB, nullable=False)

    notifications_sent = relationship(
        "NotificationSentORM",
        back_populates="notification",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.title}>"