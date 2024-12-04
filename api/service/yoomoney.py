from yoomoney import Quickpay
from api.configuration.config import settings
from uuid import uuid4
import hashlib

from api.exceptions.base import InvalidPaymentHashError


class YooMoney:
    def __init__(
        self,
        receiver: int,
        quickpay_form: str,
        payment_type: str,
        notification_secret: str,
    ):
        self.receiver = receiver
        self.quickpay_form = quickpay_form
        self.payment_type = payment_type
        self.notification_secret = notification_secret

    def create_payment_url(self, amount: float, target: str = "") -> tuple:
        quickpay = Quickpay(
            receiver=str(self.receiver),
            quickpay_form=self.quickpay_form,
            targets=target,
            paymentType=self.payment_type,
            sum=amount,
            label=str(uuid4()),
        )
        return quickpay.redirected_url, quickpay.label

    def verify_payment(self, notification_data: dict) -> bool:
        params = [
            str(notification_data["notification_type"]),
            str(notification_data["operation_id"]),
            str(notification_data["amount"]),
            str(notification_data["currency"]),
            str(notification_data["datetime"]),
            str(notification_data["sender"]),
            str(notification_data["codepro"]),
            str(self.notification_secret),
            str(notification_data["label"]),
        ]
        print(params)
        params_string = "&".join(params)
        calculated_hash = hashlib.sha1(params_string.encode("utf-8")).hexdigest()
        print(calculated_hash)
        if calculated_hash != notification_data["sha1_hash"]:
            raise InvalidPaymentHashError("The payment hash is invalid.")
        return True


yoomoney = YooMoney(
    settings.YOOMONEY_RECEIVER,
    settings.YOOMONEY_QUIQPAY_FORM,
    settings.YOOMONEY_PAYMENT_TYPE,
    settings.YOOMONEY_NOTIFICATION_SECRET,
)
