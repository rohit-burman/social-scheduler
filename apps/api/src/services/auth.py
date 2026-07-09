from datetime import UTC,datetime
from src.core.secutity import hash_password,verify_password
from src.db.repositories import UserRepository
from src.models.user import UserResponse,UserCreate,LoginRequest
from typing import Any


class AuthService:
    def __init__(self,repository: UserRepository)->None:
        self.repository = repository

    async def register(self,user_data:UserCreate)->UserResponse:
        now = datetime.now(UTC)
        doc = {
            "email":str(user_data.email).lower(),
            "password_hash":hash_password(user_data.password),
            "name":user_data.name,
            "is_active":True,
            "created_at":now
        }
        user = await self.repository.create(doc)

        return UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"],
            is_active=user["is_active"],
            created_at=user["created_at"]
        )

    async def authenticate(self, user_data:LoginRequest)->dict[str,Any] | None:

        user = await self.repository.get_by_email(str(user_data.email).lower())
        if not user or not user["is_active"]:
            return None

        if not verify_password(user_data.password,user["password_hash"]):
            return None

        return user









