from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    String,
    ForeignKey,
    DateTime,
    Text,
    Integer,
    SmallInteger,
)
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.associations import (
    push_token_genre_association,
    push_token_tag_association,
    event_tag_association,
    exhibition_tag_association,
    push_token_visitor_category_association,
)


class EventORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(Text)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)
    date_start = Column(DateTime, nullable=False)
    payment_url = Column(String, nullable=True)
    is_free = Column(Boolean, nullable=False)
    privilege_ticket = Column(Boolean, nullable=False, default=False)
    pushkin_card = Column(Boolean, nullable=False)
    min_price = Column(Integer, nullable=True)
    pinned_order = Column(SmallInteger, nullable=True, default=None)

    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=False)
    genre_id = Column(BigInteger, ForeignKey("genre.id"), nullable=False)
    visitor_category_id = Column(
        BigInteger, ForeignKey("visitor_category.id"), nullable=False
    )
    category_id = Column(BigInteger, ForeignKey("category.id"), nullable=True)

    visitor_category = relationship(
        "VisitorCategoryORM",
        back_populates="events",
        lazy="selectin",
    )

    genre = relationship(
        "GenreORM",
        back_populates="events",
        lazy="selectin",
    )

    location = relationship(
        "LocationORM",
        back_populates="events",
        lazy="selectin",
    )

    tags = relationship(
        "TagORM",
        secondary=event_tag_association,
        back_populates="events",
        lazy="selectin",
    )

    category = relationship(
        "CategoryORM",
        back_populates="events",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class ExhibitionORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    description = Column(String)
    image_url = Column(String, nullable=True)
    disabilities = Column(Boolean, default=False)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)
    payment_url = Column(String, nullable=True)
    min_price = Column(Integer, nullable=True)
    is_free = Column(Boolean, nullable=False)
    privilege_ticket = Column(Boolean, nullable=False)
    pushkin_card = Column(Boolean, nullable=False)
    audio_guide = Column(Boolean, nullable=False)
    pinned_order = Column(SmallInteger, nullable=True, default=None)

    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=False)
    visitor_category_id = Column(
        BigInteger, ForeignKey("visitor_category.id"), nullable=False
    )
    category_id = Column(BigInteger, ForeignKey("category.id"), nullable=True)

    visitor_category = relationship(
        "VisitorCategoryORM",
        back_populates="exhibitions",
        lazy="selectin",
    )

    location = relationship(
        "LocationORM",
        back_populates="exhibitions",
        lazy="selectin",
    )

    tags = relationship(
        "TagORM",
        secondary=exhibition_tag_association,
        back_populates="exhibitions",
        lazy="selectin",
    )

    category = relationship(
        "CategoryORM",
        back_populates="exhibitions",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class VisitorCategoryORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        back_populates="visitor_category",
        lazy="selectin",
    )

    exhibitions = relationship(
        "ExhibitionORM",
        back_populates="visitor_category",
        lazy="selectin",
    )

    push_tokens = relationship(
        "PushTokenORM",
        secondary=push_token_visitor_category_association,
        back_populates="visitor_categories",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class GenreORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        back_populates="genre",
        lazy="selectin",
    )

    push_tokens = relationship(
        "PushTokenORM",
        secondary=push_token_genre_association,
        back_populates="genres",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class TagORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        secondary=event_tag_association,
        back_populates="tags",
        lazy="selectin",
    )

    exhibitions = relationship(
        "ExhibitionORM",
        secondary=exhibition_tag_association,
        back_populates="tags",
        lazy="selectin",
    )

    push_tokens = relationship(
        "PushTokenORM",
        secondary=push_token_tag_association,
        back_populates="tags",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class CategoryORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    events = relationship(
        "EventORM",
        back_populates="category",
        lazy="selectin",
    )
    exhibitions = relationship(
        "ExhibitionORM",
        back_populates="category",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"
