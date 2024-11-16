import httpx

from api.configuration.config import settings


class WhatsAppBot:
    def __init__(self, instance_id, api_token):
        super().__init__()
        self.instance_id = instance_id
        self.api_token = api_token
        self.api_url = settings.API_URL

    async def send_message(self, phone_number, message):
        url = (
            f"{self.api_url}/waInstance{self.instance_id}/sendMessage/{self.api_token}"
        )
        payload = {"chatId": f"{phone_number}@c.us", "message": message}
        headers = {"Content-Type": "application/json"}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
        return response.json()


whatsapp_bot = WhatsAppBot(settings.INSTANCE_ID, settings.API_TOKEN)
