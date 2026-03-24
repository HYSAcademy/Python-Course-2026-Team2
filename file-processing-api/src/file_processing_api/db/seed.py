import asyncio
from datetime import datetime, UTC

from file_processing_api.db.models import Archive, File
from file_processing_api.db.session import async_session


async def add_sample_data():
    async with async_session() as session:
        archive = Archive(filename="my_archive.zip", uploaded_at=datetime.now(UTC))
        session.add(archive)
        await session.commit()
        await session.refresh(archive)

        file = File(
            archive_id=archive.id,
            filename="file1.txt",
            content="Hello, world!",
            path="/storage/files/file1.txt",
        )
        session.add(file)
        await session.commit()
        print(f"Inserted archive id={archive.id} and file id={file.id}")


if __name__ == "__main__":
    asyncio.run(add_sample_data())
