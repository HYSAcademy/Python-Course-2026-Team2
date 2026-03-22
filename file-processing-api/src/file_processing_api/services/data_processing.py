import uuid

import aiofiles
from fastapi import UploadFile
from loguru import logger

from file_processing_api.db.models import Archive, File
from sqlmodel.ext.asyncio.session import AsyncSession

import asyncio
import zipfile
import io

CHUNK_SIZE = 1024 * 1024
semaphore = asyncio.Semaphore(25)


def extract_files(content: bytes):
    extracted = []

    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        for filename in zip_ref.namelist():
            clean_filename = filename.split('/')[-1]

            if not clean_filename:
                continue

            with zip_ref.open(filename) as f:
                text = f.read().decode("utf-8")
                extracted.append((clean_filename, text))

    return extracted


async def process_archive(archive_name: str, contents: bytes, session: AsyncSession):
    archive = Archive(filename=archive_name)
    session.add(archive)

    await session.flush()  # get archive.id

    extracted = await asyncio.to_thread(extract_files, contents)

    for name, text in extracted:
        db_file = File(
            archive_id=archive.id,
            filename=name,
            content=text
        )
        session.add(db_file)

    return [{"filename": name, "content": text} for name, text in extracted]


async def upload_file(filename: str, text: str) -> str:
    path = f"/storage/files/{uuid.uuid4()}_{filename}"
    logger.info(path, "PATH")

    async with semaphore:
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(text)

    return text
