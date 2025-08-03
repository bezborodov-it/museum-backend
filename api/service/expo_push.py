import httpx

from api.configuration.config import settings

HEADERS = {"Content-Type": "application/json"}


class ExpoPushNotification:

    def __init__(self):
        self.url = settings.EXPO_NOTIFICATIONS_URL

    async def send_personal_message(self, push_token: str, title: str, body: str, data: dict = None):
        payload = {
            "to": f"ExponentPushToken[{push_token}]",
            "title": title,
            "body": body
        }
        if data is not None:
            payload['data'] = data
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, headers=HEADERS, json=payload)
        return response.json()

    async def send_mass_message(self, push_tokens: list, title: str, body: str, data: dict = None):
        results = []
        for i in range(0, len(push_tokens), 100):
            batch = push_tokens[i:i + 100]
            payload = {
                "to": [f"ExponentPushToken[{token}]" for token in batch],
                "title": title,
                "body": body,
            }
            if data is not None:
                payload['data'] = data

            async with httpx.AsyncClient() as client:
                response = await client.post(self.url, headers=HEADERS, json=payload)
                results.append(response.json())
        return results


expo_push_notification = ExpoPushNotification()
