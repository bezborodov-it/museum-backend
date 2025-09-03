from api.cruds.base import Base, with_model
from api.models import NotificationORM


@with_model(NotificationORM)
class Notification(Base):
    pass
