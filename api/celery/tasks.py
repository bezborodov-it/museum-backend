from api.celery.worker import celery
from api.service import expo_push_notification
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@celery.task(name="send_mass_push")
def send_mass_push(notification_id: int, tokens: list, title: str, body: str):
    try:
        responses = expo_push_notification.send_mass_message(tokens, title, body)
        logger.info(
            f"Push notification sent for notification_id={notification_id} | "
            f"tokens={tokens} | responses={responses}"
        )
        return {"Sent notifications to": len(tokens)}
    except Exception as e:
        logger.error(f"Push notification failed for notification_id={notification_id}: {e}", exc_info=True)
        return {"error": str(e)}
