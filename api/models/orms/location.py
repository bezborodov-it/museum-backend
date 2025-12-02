from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    String,
    Text,
    ForeignKey,
    Integer,
    Float,
)
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.associations import location_accessibility


class LocationORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    working_hours = Column(String, nullable=True)
    working_days = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    address = Column(String, nullable=False)
    phones = Column(String, nullable=True)
    about = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=True)

    events = relationship(
        "EventORM",
        back_populates="location",
        lazy="selectin",
    )
    exhibitions = relationship(
        "ExhibitionORM",
        back_populates="location",
        lazy="selectin",
    )
    accessibilities = relationship(
        "AccessibilityORM",
        secondary=location_accessibility,
        lazy="selectin",
    )
    floors = relationship(
        "NavigationFloorORM",
        back_populates="location",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="NavigationFloorORM.floor_num"
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"


class AccessibilityORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.name}>"
