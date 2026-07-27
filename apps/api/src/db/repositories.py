from datetime import datetime, UTC
from typing import Any

from bson import ObjectId
from pymongo.asynchronous.client_session import AsyncClientSession
from pymongo.asynchronous.database import AsyncDatabase


class UserRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self.collection = db["users"]

    async def create(self, document: dict[str, Any]) -> dict[str, Any]:
        res = await self.collection.insert_one(document)
        document["_id"] = res.inserted_id  # pymongo does this automatically so we do not have to do it
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

    async def rotate(self, old_jti: str, new_doc: dict[str, Any], used_at: datetime) -> bool:
        client = self.collection.database.client

        async def callback(session) -> bool:
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


class WorkspaceRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db["workspaces"]

    async def create(self, document: dict[str, Any],session:AsyncClientSession|None =None) -> str:
        res = await self.collection.insert_one(document,session=session)
        return str(res.inserted_id)

    async def get_by_id(self, workspace_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(workspace_id): return None
        return await self.collection.find_one({'_id': ObjectId(workspace_id)})

    # async def get_by_ids(self,workspace_ids: list[ObjectId]) -> list[dict[str, Any]]:
    #     pass

    async def get_by_slug(self, slug: str) -> dict[str, Any] | None:
        return await self.collection.find_one({'slug': slug})

    async def delete(self, workspace_id: str) -> bool:
        if not ObjectId.is_valid(workspace_id):
            return False
        res = await self.collection.delete_one({'_id': ObjectId(workspace_id)})
        if res.deleted_count < 1:
            return False
        else:
            return True

    async def update_name(self, workspace_id: str, new_name: str) -> bool:
        res = await self.collection.update_one(
            {
                '_id': ObjectId(workspace_id)
            },
            {
                '$set': {
                    'name': new_name
                }
            }
        )
        return res.matched_count > 0


class WorkspaceMemberRepository:
    def __init__(self, db: AsyncDatabase) -> None:
        self.collection = db['workspace_members']

    async def create(self, document: dict[str, Any],session:AsyncClientSession|None=None) -> str:
        res = await self.collection.insert_one(document,session=session)
        return str(res.inserted_id)

    async def get_membership(self, workspace_id: str, user_id: str) -> dict[str, Any] | None:
        if not ObjectId.is_valid(workspace_id) or not ObjectId.is_valid(user_id):
            return None
        return await self.collection.find_one({
            'workspace_id': ObjectId(workspace_id),
            'user_id': ObjectId(user_id)
        })

    async def list_by_user(self, user_id: str) -> list[dict[str, Any]]:
        if not ObjectId.is_valid(user_id):
            return []

        res = await self.collection.find({
            'user_id': ObjectId(user_id)
        }).to_list()

        return res
