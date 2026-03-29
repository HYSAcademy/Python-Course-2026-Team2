import json
import uuid

import aiofiles
from fastapi import UploadFile
from sqlalchemy.dialects.postgresql import insert

from services.api_service.app.db.session import async_session
from services.api_service.app.db.models import Archive, File
from services.api_service.app.services.file_validation import FileValidationService
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
        )
        for data in uploaded_files
    ]
    session.add_all(files)

    publish_message("files_uploaded", {"archive_id": archive.id})

    return [{"filename": name, "content": text} for name, text in extracted]


async def upload_file(file_data: tuple[str, str]) -> dict:
    filename, text = file_data
    path = f"/storage/files/{uuid.uuid4()}_{filename}"

    async with FILE_WRITE_SEMAPHORE:
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(text)

    return {"filename": filename, "content": text, "path": path}


async def save_vector(file_id: int, vector, session: AsyncSession) -> None:
    vector_dict = dict(zip(vector.indices.tolist(), vector.data.tolist()))

    stmt = (
        insert(FileVector)
        .values(file_id=file_id, vector=vector_dict)
        .on_conflict_do_update(
            index_elements=[
                "file_id"
            ],  # <- use index/column instead of constraint name
            set_={"vector": vector_dict},
        )
    )

    await session.exec(stmt)


semaphore = asyncio.Semaphore(10)


async def save_vector_parallel(file_id: int, vector):
    async with semaphore:
        async with async_session() as session:
            await save_vector(file_id, vector, session)
            await session.commit()
