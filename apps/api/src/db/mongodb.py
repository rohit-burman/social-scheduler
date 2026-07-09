from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase
from src.settings import settings
from src.db.indexes import create_indexes
client : AsyncMongoClient | None = None
db : AsyncDatabase | None = None

async def connect_to_db()-> None:
    global client
    global db
    client = AsyncMongoClient(settings.mongodb_url)
    await client.admin.command("ping")
    db = client[settings.mongodb_db_name]
    # await create_indexes(db)

async def close_db()-> None:
    global client
    global db

    if client is not None:
        await client.close()

    client = None
    db = None

def get_db()->AsyncDatabase:
    if db is None:
        raise RuntimeError("db not started")
    return db

