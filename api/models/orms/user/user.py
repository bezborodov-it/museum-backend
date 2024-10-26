from sqlalchemy import BigInteger, String, Column, Enum, ForeignKey, Table
from sqlalchemy.orm import relationship

from api.models.orms.base import BaseORM
from api.models.mixin.date import DateORMMixin
from api.models.associations import (
    user_genre_preference_association,
    user_tag_preference_association,
)


class UserORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=True, unique=True)
    number = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=True)

    roles = relationship(
        "UserRoleORM",
        back_populates="user",
        foreign_keys="[UserRoleORM.user_id]",
        lazy="selectin",
    )

    refresh_tokens = relationship(
        "RefreshTokenORM",
        back_populates="user",
        foreign_keys="[RefreshTokenORM.user_id]",
        lazy="selectin",
    )

    genres = relationship(
        "EventGenreORM",
        secondary=user_genre_preference_association,
        back_populates="users",
        lazy="selectin",
    )

    tags = relationship(
        "EventTagORM",
        secondary=user_tag_preference_association,
        back_populates="users",
        lazy="selectin",
    )

    tickets = relationship("TicketORM", back_populates="user", lazy="selectin")

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.name} {self.number}>"
