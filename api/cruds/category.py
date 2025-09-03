from api.cruds.base import Base, with_model
from api.models.orms.event import CategoryORM


@with_model(CategoryORM)
class Category(Base):
    pass
