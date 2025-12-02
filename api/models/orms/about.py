from sqlalchemy import (
    BigInteger,
    Column,
    String,
)

from api.models.orms.base import BaseORM


class AboutORM(BaseORM):
    id = Column(BigInteger, primary_key=True)
    phone = Column(String, nullable=True)
    site_url = Column(String, nullable=True)
    email = Column(String, nullable=True)
