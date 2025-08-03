from sqlalchemy import (
    BigInteger,
    Column,
    ForeignKey,
    String,
    Enum
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from api.models import DateORMMixin
from api.models.enums import NotificationTypeEnum
from api.models.orms.base import BaseORM

class NotificationSentORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    push_token_id = Column(BigInteger, ForeignKey("push_token.id"), nullable=False)
    notification_id = Column(BigInteger, ForeignKey("notification.id"), nullable=False)
    type = Column(Enum(NotificationTypeEnum, name="notification_type_enum"), nullable=False)
    status = Column(String(5), nullable=False)
    result = Column(JSONB, nullable=False)

    push_token = relationship(
        "PushTokenORM",
        back_populates="notifications",
        lazy="selectin",
    )

    notification = relationship(
        "NotificationORM",
        back_populates="notifications_sent",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.push_token_id}>"