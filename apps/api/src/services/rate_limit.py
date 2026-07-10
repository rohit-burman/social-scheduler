from redis.asyncio import Redis


class LoginRateLimiter:
    def __init__(self, redis: Redis, limit: int = 5, window_secs: int = 900) -> None:
        self.redis = redis
        self.limit = limit
        self.window_secs = window_secs

    RECORD_FAILURE_SCRIPT="""
    local count=redis.call("INCR",KEYS[1])
    if count == 1 then
        redis.call("EXPIRE",KEYS[1],ARGV[1])
    end
    return count
    """
    async def is_limited(self, key: str) -> bool:
        count = await self.redis.get(key)
        if count is None:
            return False
        return int(count) >= self.limit

    async def record_failure(self, key: str) -> int:
        # count = await self.redis.incr(key) # better to use lua scripting to ensure atomicity.It runs on Redis and not on python
        count = await self.redis.eval(self.RECORD_FAILURE_SCRIPT,1,key,self.window_secs)
        return int(count)

    async def clear(self, key: str) -> None:
        await self.redis.delete(key)


def build_login_failure_key(client_ip: str, email: str) -> str:
    normalized_email = email.strip().lower()
    return f"rate_limit:login:failure:{client_ip}:{normalized_email}"
