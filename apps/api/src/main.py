from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.db.mongodb import (connect_to_db,close_db)
from src.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI)-> AsyncIterator[None]:
    await connect_to_db()
    yield
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
