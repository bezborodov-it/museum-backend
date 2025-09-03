from api.cruds.base import Base, with_model
from api.models import TagORM


@with_model(TagORM)
class Tag(Base):
    pass
