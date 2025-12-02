import httpx

from api.configuration.config import settings

HEADERS = {"Content-Type": "application/json"}


class ExpoPushNotification:

    def __init__(self):
        self.url = settings.EXPO_NOTIFICATIONS_URL

    def send_mass_message(self, push_tokens: list, title: str, body: str):
        results = []
        with httpx.Client() as client:
            for i in range(0, len(push_tokens), 100):
                batch = push_tokens[i : i + 100]
                payload = {
                    "to": [f"{token}" for token in batch],
                    "title": title,
                    "body": body,
                }

                response = client.post(self.url, headers=HEADERS, json=payload)
                results.append(response.json())
        return results


expo_push_notification = ExpoPushNotification()
