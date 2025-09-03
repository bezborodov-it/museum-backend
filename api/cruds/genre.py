from api.cruds.base import Base, with_model
from api.models import GenreORM


@with_model(GenreORM)
class Genre(Base):
    pass
