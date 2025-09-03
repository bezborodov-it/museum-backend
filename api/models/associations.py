from sqlalchemy import Column, ForeignKey, Table
from api.models.orms.base import BaseORM

event_tag_association = Table(
    "event_tag_association",
    BaseORM.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

exhibition_tag_association = Table(
    "exhibition_tag_association",
    BaseORM.metadata,
    Column(
        "exhibition_id",
        ForeignKey("exhibition.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

push_token_genre_association = Table(
    "push_token_genre_association",
    BaseORM.metadata,
    Column(
        "push_token_id",
        ForeignKey("push_token.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("genre_id", ForeignKey("genre.id", ondelete="CASCADE"), primary_key=True),
)

push_token_tag_association = Table(
    "push_token_tag_association",
    BaseORM.metadata,
    Column(
        "push_token_id",
        ForeignKey("push_token.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

push_token_visitor_category_association = Table(
    "push_token_visitor_category_association",
    BaseORM.metadata,
    Column(
        "push_token_id",
        ForeignKey("push_token.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "visitor_category_id",
        ForeignKey("visitor_category.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
