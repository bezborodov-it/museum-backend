from sqlalchemy import BigInteger, Column, String, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship

from api.models.mixin.date import DateORMMixin
from api.models.orms.base import BaseORM


class InclusiveStoryORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False)
    location_id = Column(BigInteger, ForeignKey("location.id"), nullable=False)

    location = relationship(
        "LocationORM",
        back_populates="inclusive_story"
    )
    stories = relationship(
        "StoryORM",
        back_populates="inclusive_story",
        lazy="selectin",
        cascade="all, delete-orphan",
        order_by="StoryORM.order"
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.title}>"


class StoryORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    story_image_url = Column(String, nullable=True)
    order = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)

    inclusive_story_id = Column(BigInteger, ForeignKey("inclusive_story.id"), nullable=False)

    inclusive_story = relationship(
        "InclusiveStoryORM",
        back_populates="stories"
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id}>"
