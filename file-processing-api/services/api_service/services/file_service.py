from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from services.api_service.db.models import File
from services.api_service.db import get_session


async def get_all_files(session: AsyncSession):
    result = await session.exec(select(File))

    return result.all()

def get_files_by_archive_id(archive_id: int, session):
    result = session.exec(select(File).where(File.archive_id == archive_id))

    return result.all()