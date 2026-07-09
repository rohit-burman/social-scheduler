from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from jwt import InvalidTokenError
from pymongo.asynchronous.database import AsyncDatabase
from src.db.mongodb import get_db
from src.db.repositories import UserRepository
from src.services.auth import AuthService
from src.core.secutity import oauth2_scheme, decode_access_token

DatabaseDep = Annotated[AsyncDatabase, Depends(get_db)]


def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)


UserRepoDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_auth_services(repo: UserRepoDep) -> AuthService:
    return AuthService(repo)


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
        payload = decode_access_token(token)
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
