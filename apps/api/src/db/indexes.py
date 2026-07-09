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
