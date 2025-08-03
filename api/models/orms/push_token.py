from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    String
)
from sqlalchemy.orm import relationship

from api.models import DateORMMixin
from api.models.orms.base import BaseORM

class PushTokenORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)
    expo_push_token = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default='true')
    last_used = Column(DateTime, nullable=True)

    user = relationship(
        "UserORM",
        back_populates="push_token",
        lazy="selectin",
    )

    notifications = relationship(
        "NotificationORM",
        back_populates="push_token",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.user_id} {self.id}>"