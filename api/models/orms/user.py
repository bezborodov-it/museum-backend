from sqlalchemy import BigInteger, String, Column

from api.models.orms.base import BaseORM
from api.models.mixin.date import DateORMMixin


class UserORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    login = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.login}>"
