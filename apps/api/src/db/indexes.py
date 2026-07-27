from enum import unique

from pymongo import ASCENDING
from pymongo.asynchronous.database import AsyncDatabase

async def create_indexes(db :AsyncDatabase)->None:
    await db["users"].create_index(
        # [("email",ASCENDING)],
        "email",
        unique=True,
        name="user_email"
    )

    await db["refresh_sessions"].create_index(
        "expires_at",
        expireAfterSeconds=0 # 0 means
    )

    await db["refresh_sessions"].create_index(
        "jti",
        unique=True
    )

    await db["refresh_sessions"].create_index(
        "family_id"
    )

    await db["refresh_sessions"].create_index(
        "user_id"
    )

    await db["workspaces"].create_index(
        "slug",
        unique=True,
        name="workspace_slug"
    )

    await db["workspace_members"].create_index(
        keys=[("workspace_id",ASCENDING),("user_id",ASCENDING)],
        unique=True,
        name="workspace_id_user_id"
    )

    await db["posts"].create_index(
        keys=[("workspace_id",ASCENDING),("status",ASCENDING)],
        name="workspace_status"
    )

    await db["posts"].create_index(
        keys=[("workspace_id",ASCENDING),("provider_type",ASCENDING)],
        name="workspace_provider"
    )
