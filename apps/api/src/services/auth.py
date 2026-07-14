from src.core.security import hash_password, verify_password, create_access_token, create_refresh_token, hash_token
from src.db.repositories import UserRepository, RefreshSessionRepository
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
        refresh_token = create_refresh_token(user_id, refresh_jti, family_id,now,expires_at)

        session_doc = {
            "user_id": user_id,
            "jti": refresh_jti,
            "token_hash": hash_token(refresh_token),
            "expires_at":expires_at,
            "used_at": None,
            "revoked_at": None,
            "replaced_bt_jti": None,
            "created_at": now
        }
        await self.refresh_session_repository.create(session_doc)
        return access_token, refresh_token
