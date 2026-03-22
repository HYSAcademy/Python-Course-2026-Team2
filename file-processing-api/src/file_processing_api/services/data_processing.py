import uuid

import aiofiles

from file_processing_api.db.models import Archive, File, FileVector
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
    uploaded_files = await asyncio.gather(*[
        upload_file(file_data) for file_data in extracted
    ])

    for data in uploaded_files:
        db_file = File(
            archive_id=archive.id,
            filename=data["filename"],
            path=data["path"],
            content=data["content"]
        )
        session.add(db_file)

    return [{"filename": name, "content": text} for name, text in extracted]


async def upload_file(file_data: tuple[str, str]) -> dict:
    filename, text = file_data
    path = f"/storage/files/{uuid.uuid4()}_{filename}"

    async with semaphore:
        async with aiofiles.open(path, "w", encoding="utf-8") as f:
            await f.write(text)

    return {
        "filename": filename,
        "content": text,
        "path": path
    }

async def save_vector(file_id: int, vector, session: AsyncSession) -> None:
    vector_dict = dict(zip(
        vector.indices.tolist(),
        vector.data.tolist()
    ))

    db_vector = FileVector(
        file_id=file_id,
        vector=vector_dict
    )
    session.add(db_vector)
