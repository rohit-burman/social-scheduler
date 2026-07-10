from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.mongodb import (connect_to_db,close_db)
from src.api.router import api_router
from src.db.redis import connect_to_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncIterator[None]:
    await connect_to_db()
    await  connect_to_redis()

    yield
    await close_redis()
    await close_db()
app = FastAPI(
    title="Social Schedular API",
    lifespan=lifespan
)

@app.get("/health")
async def health()-> dict:
    return {"status": "ok"}


app.include_router(
    api_router,
    prefix="/api/v1"
)
