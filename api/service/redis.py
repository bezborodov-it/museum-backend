import redis.asyncio as redis
from api.configuration.config import settings


class RedisService:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
        )


redis_service = RedisService()
