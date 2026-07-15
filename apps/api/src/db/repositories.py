import uuid
from datetime import datetime, UTC
from typing import Any, Optional
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.settings import settings


class UserRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self.collection = db["users"]

    async def create(self, document: dict[str, Any]) -> dict[str, Any]:
        res = await self.collection.insert_one(document)
        document["_id"] = res.inserted_id
        return document

    async def get_by_email(self, email: str) -> dict[str, Any] | None:
        return await self.collection.find_one({'email': email})

    async def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(user_id): return None
        return await self.collection.find_one({'_id': ObjectId(user_id)})


class RefreshSessionRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self.collection = db["refresh_sessions"]

    async def create(self, document: dict[str, Any]) -> dict[str, Any]:
        # now = datetime.now(UTC)
        #
        # expires_at = now + timedelta(
        #     days=settings.refresh_token_expire_days,
        # )
        # payload = {
        #     "user_id":document["user_id"],
        #     "jti":document["jti"],
        #     "family_id": document["family_id"],
        #     "token_hash": document["token_hash"],
        #     "expires_at":expires_at,
        #     "used_at": None,
        #     "revoked_at": None,
        #     "replaced_by_jti": None,
        # }
        #
        # res = await self.collection.insert_one(payload)
        # payload["_id"]=res.inserted_id
        # return payload
        result = await self.collection.insert_one(document)
        document["_id"] = result.inserted_id
        return document

    async def get_by_jti(self, jti: str) -> dict[str, Any] | None:
        return await self.collection.find_one({'jti': jti})

    async def consume_and_replace(self, jti: str, replaced_by_jti: str, used_at: datetime) -> bool:
        res = await self.collection.find_one_and_update(
            {
                'jti': jti,
                'revoked_at': None,
                'used_at': None,
                'expires_at': {'$gt': datetime.now(UTC)}
                # 'expires_at': {'$gt':used_at}
            },
            {
                "$set": {
                    'used_at': used_at,
                    'replaced_by_jti': replaced_by_jti,
                }
            }
        )
        return res is not None

    async def revoke_family(self, family_id: str, revoked_at: datetime) -> int:
        res = await self.collection.update_many(
            {
                'family_id': family_id,
                'revoked_at': None,
            },
            {"$set":
                {
                    'revoked_at': revoked_at
                }
            }
        )
        return res.modified_count

    async def rotate(self,old_jti:str,new_doc:dict[str,Any],used_at:datetime)->bool:
        client = self.collection.database.client
        rotated=False
        async def callback(session)->bool:
            old_session = await self.collection.find_one_and_update(
                {
                    'jti': old_jti,
                    'revoked_at': None,
                    'used_at': None,
                    'expires_at': {'$gt': used_at}
                },
                {
                    "$set": {
                        'used_at': used_at,
                        'replaced_by_jti': new_doc["jti"],
                    }
                },
                session=session
            )
            if old_session is None:
                return False
            await self.collection.insert_one(new_doc, session=session)
            return True

        async with client.start_session() as s:
            return await s.with_transaction(callback)
