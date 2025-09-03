from celery import Celery
from api.configuration.config import settings

celery = Celery()

celery.conf.update(
    broker_url=f"amqp://{settings.RABBIT_USER}:{settings.RABBIT_PASSWORD}@rabbitmq:5672//",
    result_backend="rpc://",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.CELERY_TIMEZONE,
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,
    task_soft_time_limit=3000,
    broker_connection_retry_on_startup=True,
)

celery.autodiscover_tasks(["api.celery.tasks"])
