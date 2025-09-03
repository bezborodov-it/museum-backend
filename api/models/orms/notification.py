from sqlalchemy import (
    BigInteger,
    Column,
    String,
    DateTime,
)

from api.models import DateORMMixin
from api.models.orms.base import BaseORM


class NotificationORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
    time_to_send = Column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.title}>"
