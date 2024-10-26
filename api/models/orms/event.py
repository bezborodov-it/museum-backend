from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.associations import (
    user_genre_preference_association,
    user_tag_preference_association,
    event_visitor_category_association,
    event_tag_association,
)


class EventORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)
    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=True)
    genre_id = Column(BigInteger, ForeignKey("event_genre.id"), nullable=True)

    visitor_category = relationship(
        "VisitorCategoryORM",
        secondary=event_visitor_category_association,
        back_populates="events",
        lazy="selectin",
    )

    genre = relationship(
        "EventGenreORM",
        back_populates="events",
        lazy="selectin",
    )

    location = relationship(
        "LocationORM",
        back_populates="events",
        lazy="selectin",
    )

    tag = relationship(
        "EventTagORM",
        secondary=event_tag_association,
        back_populates="events",
        lazy="selectin",
    )

    tickets = relationship("TicketORM", back_populates="event", lazy="selectin")

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class VisitorCategoryORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        secondary=event_visitor_category_association,
        back_populates="visitor_category",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class EventGenreORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        back_populates="genre",
        lazy="selectin",
    )

    users = relationship(
        "UserORM",
        secondary=user_genre_preference_association,
        back_populates="genres",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class EventTagORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        secondary=event_tag_association,
        back_populates="tag",
        lazy="selectin",
    )

    users = relationship(
        "UserORM",
        secondary=user_tag_preference_association,
        back_populates="tags",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"
