from api.cruds.base import Base, with_model
from api.models import AccessibilityORM


@with_model(AccessibilityORM)
class Accessibility(Base):
    pass
