from api.cruds.base import Base, with_model
from api.models import LocationORM


@with_model(LocationORM)
class Location(Base):
    pass
