from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from file_processing_api.db.models import File


async def get_files_by_archive_id(archive_id: int, session: AsyncSession):
    result = await session.exec(select(File).where(File.archive_id == archive_id))
    files = result.all()

    return files