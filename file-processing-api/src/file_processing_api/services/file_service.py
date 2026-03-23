from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from file_processing_api.db.models import File, FileVector


async def get_all_files(session: AsyncSession):
    result = await session.exec(select(File))

    return result.all()

async def get_all_vectors(session: AsyncSession):
    result = await session.exec(select(FileVector))

    return result.all()