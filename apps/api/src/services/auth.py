from hmac import compare_digest

from bson.objectid import ObjectId
from jwt import InvalidTokenError

from src.core.security import hash_password, verify_password, create_access_token, create_refresh_token, hash_token, \
    decode_token
from src.db.repositories import UserRepository, RefreshSessionRepository
from src.exceptions import RefreshTokenReuseError, InvalidRefreshTokenError
from src.models.user import UserResponse, UserCreate
from src.models.auth import LoginRequest

from datetime import UTC, datetime, timedelta
from src.settings import settings
from uuid import uuid4
from typing import Any


class AuthService:
    def __init__(self, user_repository: UserRepository, refresh_session_repository: RefreshSessionRepository) -> None:
        self.user_repository = user_repository
        self.refresh_session_repository = refresh_session_repository

    async def register(self, user_data: UserCreate) -> UserResponse:
        now = datetime.now(UTC)
        doc = {
            "email": str(user_data.email).lower(),
            "password_hash": hash_password(user_data.password),
            "name": user_data.name,
            "is_active": True,
            "created_at": now
        }
        user = await self.user_repository.create(doc)

        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            is_active=user["is_active"],
            created_at=user["created_at"]
        )

    async def authenticate(self, user_data: LoginRequest) -> dict[str, Any] | None:

        user = await self.user_repository.get_by_email(str(user_data.email).lower())
        if not user or not user["is_active"]:
            return None

        if not verify_password(user_data.password, user["password_hash"]):
            return None

        return user

    async def issue_token_pair(self, user_id: str) -> tuple[str, str]:
        family_id = str(uuid4())
        refresh_jti = str(uuid4())
        now = datetime.now(UTC)
        expires_at = now + timedelta(days=settings.refresh_token_expire_days)
        access_token = create_access_token(user_id)
        refresh_token = create_refresh_token(user_id, refresh_jti, family_id, now, expires_at)

        session_doc = {
            "user_id": ObjectId(user_id),
            "jti": refresh_jti,
            "family_id":family_id,
            "token_hash": hash_token(refresh_token),
            "expires_at": expires_at,
            "used_at": None,
            "revoked_at": None,
            "replaced_bt_jti": None,
            "created_at": now
        }
        await self.refresh_session_repository.create(session_doc)
        return access_token, refresh_token

    async def rotate_refresh_token(self, refresh_token: str) -> tuple[str, str]:
        now = datetime.now(UTC)

        payload = decode_token(refresh_token)

        token_type = payload.get("type")
        user_id = payload.get("sub")
        jti = payload.get("jti")
        family_id = payload.get("family_id")

        if not isinstance(token_type, str) or token_type != "refresh":
            raise InvalidTokenError("Invalid token type")
        if not isinstance(user_id, str) or not user_id:
            raise InvalidTokenError("missing user")
        if not isinstance(jti, str) or not jti:
            raise InvalidTokenError("missing jti")
        if not isinstance(family_id, str) or not family_id:
            raise InvalidTokenError("missing family_id")

        session = await self.refresh_session_repository.get_by_jti(jti)

        if session is None:
            raise InvalidTokenError("invalid jti")
        if session.get("user_id") != ObjectId(user_id):  # todo check
            raise InvalidTokenError("Invalid user")
        if session.get("family_id") != family_id:
            raise InvalidTokenError("Invalid family id")
        if not isinstance(session.get("token_hash"), str):
            raise InvalidTokenError("Invalid refresh token")
        if not compare_digest(session.get("token_hash"), hash_token(refresh_token)):
            raise InvalidTokenError("Invalid refresh token")
        if session.get("revoked_at") is not None:
            raise InvalidTokenError("Invalid refresh token")
        if session.get("expires_at") <= now:
            raise InvalidTokenError("Invalid refresh token")

        if session.get("used_at") is not None:
            await self.refresh_session_repository.revoke_family(family_id=session.get("family_id"), revoked_at=now)
            raise RefreshTokenReuseError()

        new_jti = str(uuid4())
        new_family_id = family_id
        expires_at = now + timedelta(days=settings.refresh_token_expire_days)

        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id, new_jti, new_family_id, issued_at=now, expires_at=expires_at)

        replacement_doc = {
            "user_id": ObjectId(user_id),
            "jti": new_jti,
            "family_id": new_family_id,
            "token_hash": hash_token(new_refresh_token),
            "expires_at": expires_at,
            "used_at": None,
            "revoked_at": None,
            "replaced_by_jti": None,
            "created_at": now
        }

        rotated = await self.refresh_session_repository.rotate(old_jti=jti, new_doc=replacement_doc, used_at=now)

        if not rotated:
            latest_session = await self.refresh_session_repository.get_by_jti(jti)

            if latest_session and latest_session.get("used_at") is not None:
                await self.refresh_session_repository.revoke_family(family_id=family_id, revoked_at=now, )
                raise RefreshTokenReuseError()
            raise InvalidRefreshTokenError()

        return new_access_token, new_refresh_token
