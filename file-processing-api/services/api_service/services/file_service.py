from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from services.api_service.app.db.models import File, FileVector
from services.api_service.app.db import get_session


async def get_all_files(session: AsyncSession):
    result = await session.exec(select(File))

    return result.all()


async def get_all_vectors(session: AsyncSession):
    result = await session.exec(select(FileVector))

    return result.all()

async def get_files_by_archive_id(archive_id: int, session: AsyncSession):
    result = await session.exec(select(File).where(File.archive_id == archive_id))

    return result.all()