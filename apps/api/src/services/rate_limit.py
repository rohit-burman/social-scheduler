from src.api.deps import RedisDep


class LoginRateLimit:
    def __init__(self,token:str):
        self.token = token


    async def is_limited(self,redis:RedisDep)->bool:
        pass

    async def record_failure(self)->None:
        pass

    async def clear(self)->None:
        pass
