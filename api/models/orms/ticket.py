from sqlalchemy import (
    Integer,
    BigInteger,
    Boolean,
    Column,
    String,
    ForeignKey,
    Table,
    Enum,
    DateTime,
)
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.enums import TicketTypeEnum, TicketStatusEnum


class TicketORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    event_id = Column(BigInteger, ForeignKey("event.id"), nullable=False)
    customer_id = Column(BigInteger, ForeignKey("user.id"), nullable=True)
    status = Column(Enum(TicketStatusEnum), default=TicketStatusEnum.available)
    type = Column(Enum(TicketTypeEnum), nullable=False)
    price = Column(Integer, nullable=False)
    booked_at = Column(DateTime, nullable=True)
    purchased_at = Column(DateTime, nullable=True)
    event_date = Column(DateTime, nullable=False)
    transaction_label = Column(String, nullable=True)

    event = relationship("EventORM", back_populates="tickets", lazy="selectin")
    user = relationship(
        "UserORM",
        back_populates="tickets",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.event_id} {self.status} {self.price}>"
