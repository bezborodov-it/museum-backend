from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from api.models import DateORMMixin
from api.models.orms.base import BaseORM
from api.models.associations import (
    push_token_genre_association,
    push_token_tag_association,
    push_token_visitor_category_association,
)


class PushTokenORM(BaseORM, DateORMMixin):
    id = Column(BigInteger, primary_key=True)
    push_token = Column(String, unique=True, nullable=False)

    genres = relationship(
        "GenreORM",
        secondary=push_token_genre_association,
        back_populates="push_tokens",
        lazy="selectin",
    )

    tags = relationship(
        "TagORM",
        secondary=push_token_tag_association,
        back_populates="push_tokens",
        lazy="selectin",
    )

    visitor_categories = relationship(
        "VisitorCategoryORM",
        secondary=push_token_visitor_category_association,
        back_populates="push_tokens",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<{self.__tablename__} {self.id} {self.push_token}>"
