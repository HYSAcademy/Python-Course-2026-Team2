import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from services.api_service.db.session import async_session
from services.api_service.db.models import Archive, File
from services.api_service.services.file_validation import FileValidationService
from redis_client.publisher import publish_message


from sqlmodel.ext.asyncio.session import AsyncSession

import asyncio
import zipfile
import io


CHUNK_SIZE = 1024 * 1024
ARCHIVE_SEMAPHORE = asyncio.Semaphore(8)
FILE_WRITE_SEMAPHORE = asyncio.Semaphore(24)


async def handle_archive(archive: UploadFile, session_factory) -> None:
    async with ARCHIVE_SEMAPHORE:
        await FileValidationService.validate(archive)
        contents = await archive.read()

        async with session_factory() as session:
            async with session.begin():
                await process_archive(archive.filename, contents, session)

def extract_files(content: bytes):
    extracted = []

    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        for filename in zip_ref.namelist():
            clean_filename = filename.split("/")[-1]

            if not clean_filename:
                continue

            with zip_ref.open(filename) as f:
                text = f.read().decode("utf-8")
                extracted.append((clean_filename, text))

    return extracted


async def process_archive(archive_name: str, contents: bytes, session: AsyncSession):
    archive = Archive(filename=archive_name)
    session.add(archive)

    await session.flush()

    extracted = await asyncio.to_thread(extract_files, contents)
    uploaded_files = await asyncio.gather(
        *[upload_file(file_data) for file_data in extracted]
    )

    files = [
        File(
            archive_id=archive.id,
            filename=data["filename"],
            path=data["path"],
            content=data["content"]
        )
        for data in uploaded_files
    ]
    session.add_all(files)
    publish_message("files_uploaded", {"archive_id": archive.id})

    return [{"filename": name, "content": text} for name, text in extracted]


async def upload_file(file_data: tuple[str, str]) -> dict:
    filename, text = file_data
    relative_path = f"files/{uuid.uuid4()}_{filename}"
    full_path =f"/storage/{relative_path}"

    async with FILE_WRITE_SEMAPHORE:
        async with aiofiles.open(full_path, "w", encoding="utf-8") as f:
            await f.write(text)

    return {"filename": filename, "content": text, "path": relative_path}
