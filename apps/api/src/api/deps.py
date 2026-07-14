from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from pymongo.asynchronous.database import AsyncDatabase
from redis.asyncio import Redis

from src.db.mongodb import get_db
from src.db.redis import get_redis
from src.db.repositories import UserRepository, RefreshSessionRepository
from src.services.auth import AuthService
from src.core.security import oauth2_scheme, decode_token
from src.services.rate_limit import LoginRateLimiter

DatabaseDep = Annotated[AsyncDatabase, Depends(get_db)]


def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)

def get_refresh_session_repository(db: DatabaseDep) -> RefreshSessionRepository:
    return RefreshSessionRepository(db)

UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]
RefreshSessionRepoDep = Annotated[RefreshSessionRepository, Depends(get_refresh_session_repository)]


def get_auth_services(user_repo: UserRepoDep,refresh_session_repo:RefreshSessionRepoDep) -> AuthService:
    return AuthService(user_repo,refresh_session_repo)


AuthServiceDep = Annotated[AuthService, Depends(get_auth_services)]

AccessTokenDep = Annotated[str, Depends(oauth2_scheme)]


# async def get_current_user(token:AccessTokenDep,repo:UserRepoDep)->dict[str,Any]|None:
#
#     try:
#         payload= decode_access_token(token)
#         if payload["type"] == "access":
#             user = await repo.get_by_id(user_id=payload["sub"])
#
#             return user if user and user["is_active"] else None
#
#     except InvalidTokenError:
#         raise HTTPException(starlette.status.HTTP_401_UNAUTHORIZED)

async def get_current_user(token: AccessTokenDep, repo: UserRepoDep) -> dict[str, Any]:
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            raise InvalidTokenError("Invalid token type")

        sub = payload.get("sub")
        if not isinstance(sub, str) or not sub:
            raise InvalidTokenError("Invalid token type")

        user = await repo.get_by_id(user_id=sub)
        if not user or not user.get("is_active", False):
            raise InvalidTokenError("Invalid token type")

    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    return user


CurrentUserDep = Annotated[dict[str, Any], Depends(get_current_user)]


RedisDep = Annotated[Redis,Depends(get_redis)]

def get_login_rate_limiter(redis:RedisDep)->LoginRateLimiter:
    return LoginRateLimiter(redis=redis,limit=5,window_secs=300)

LoginRateLimiterDep = Annotated[LoginRateLimiter,Depends(get_login_rate_limiter)]
