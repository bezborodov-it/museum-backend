from sqlalchemy import BigInteger, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class NavigationFloorORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    floor_num = Column(Integer, nullable=False)
    plan_image_url = Column(String, nullable=True)
    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=False)

    location = relationship("LocationORM", back_populates="floors")
    points = relationship(
        "NavigationPointORM",
        back_populates="floor",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.floor_num}>"


class NavigationPointORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    floor_id = Column(BigInteger, ForeignKey("navigation_floor.id"), nullable=False)
    number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)

    floor = relationship("NavigationFloorORM", back_populates="points")

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.title}>"
