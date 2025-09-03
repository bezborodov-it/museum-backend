from api.cruds.base import Base, with_model
from api.models import VisitorCategoryORM


@with_model(VisitorCategoryORM)
class VisitorCategory(Base):
    pass
