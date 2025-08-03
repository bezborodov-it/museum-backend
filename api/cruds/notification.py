from api.cruds.base import Base, with_model
from api.models.orms.notification.notification_sent import NotificationSentORM


@with_model(NotificationSentORM)
class Notification(Base):
    pass

