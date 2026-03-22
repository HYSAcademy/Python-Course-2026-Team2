import os

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

sync_engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")