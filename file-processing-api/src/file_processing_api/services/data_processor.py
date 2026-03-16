import zipfile
import io

from fastapi import UploadFile

from file_processing_api.db.models import Archive, File
from sqlmodel.ext.asyncio.session import AsyncSession

import asyncio
import zipfile
import io


MAX_SIZE = 5 * 1024 * 1024

def extract_zip(content: bytes):
    extracted = []

    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        for file in zip_ref.namelist():
            size = zip_ref.getinfo(file).file_size

            if not file.endswith(".txt") or size > MAX_SIZE:
                continue

            with zip_ref.open(file) as f:
                text = f.read().decode("utf-8")
                extracted.append((file, text))

    return extracted

async def process_archive(archive: UploadFile, session: AsyncSession):
    contents = await archive.read()
    archive = Archive(filename=archive.filename)
    session.add(archive)

    await session.flush()  # get archive.id

    extracted = await asyncio.to_thread(extract_zip, contents)

    for name, text in extracted:
        db_file = File(
            archive_id=archive.id,
            filename=name,
            content=text
        )
        session.add(db_file)

    return [{"filename": name, "content": text} for name, text in extracted]