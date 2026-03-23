from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from .database import engine, sync_engine
from contextlib import contextmanager
from sqlmodel import Session


async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        yield session


@contextmanager
def get_sync_session():
    with Session(sync_engine) as session:
        yield session