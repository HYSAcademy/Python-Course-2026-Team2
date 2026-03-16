import os
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)
