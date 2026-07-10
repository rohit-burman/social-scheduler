from redis.asyncio import Redis

from src.settings import settings

redis_client: Redis | None = None


async def connect_to_redis() -> None:
    global redis_client
    redis_client = Redis.from_url(settings.redis_url, decode_responses=True)
    await redis_client.ping()


async def close_redis() -> None:
    global redis_client
    if redis_client is not None:
        await redis_client.aclose()
        redis_client = None


def get_redis() -> Redis:
    global redis_client
    if redis_client is None:
        raise RuntimeError("Redis not connected")
    return redis_client
