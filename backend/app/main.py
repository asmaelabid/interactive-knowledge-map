from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.router.router import router, setup_cors
from app.core.db import async_engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
    yield
    await async_engine.dispose()

app = FastAPI(
    title="Knowledge Map API",
    description="API for managing courses and their relationships",
    version="1.0.0",
    lifespan=lifespan
)

setup_cors(app)
app.include_router(router)