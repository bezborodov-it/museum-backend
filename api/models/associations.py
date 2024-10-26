from sqlalchemy import BigInteger, Boolean, Column, String, ForeignKey, Table
from api.models.orms.base import BaseORM

event_visitor_category_association = Table(
    "event_visitor_category_association",
    BaseORM.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "visitor_category_id",
        ForeignKey("visitor_category.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)

event_tag_association = Table(
    "event_tag_association",
    BaseORM.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("event_tag.id", ondelete="CASCADE"), primary_key=True),
)

user_genre_preference_association = Table(
    "user_genre_preference_association",
    BaseORM.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "genre_id", ForeignKey("event_genre.id", ondelete="CASCADE"), primary_key=True
    ),
)

user_tag_preference_association = Table(
    "user_tag_preference_association",
    BaseORM.metadata,
    Column("user_id", ForeignKey("user.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("event_tag.id", ondelete="CASCADE"), primary_key=True),
)
