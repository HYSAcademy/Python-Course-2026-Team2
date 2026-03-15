import zipfile
import io
from file_processing_api.db.models import Archive, File
from sqlmodel.ext.asyncio.session import AsyncSession

import asyncio
import zipfile
import io

def extract_zip(content: bytes):
    extracted = []
    with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
        for name in zip_ref.namelist():
            if not name.endswith(".txt"):
                continue
            with zip_ref.open(name) as f:
                text = f.read().decode("utf-8")
                extracted.append((name, text))
    return extracted

async def process_archive(filename: str, content: bytes, session: AsyncSession):
    archive = Archive(filename=filename)
    session.add(archive)

    await session.flush()  # get archive.id

    def extract_zip():
        extracted = []
        with zipfile.ZipFile(io.BytesIO(content)) as zip_ref:
            for name in zip_ref.namelist():
                if not name.endswith(".txt"):
                    continue
                with zip_ref.open(name) as f:
                    text = f.read().decode("utf-8")
                    extracted.append((name, text))
        return extracted

    extracted = await asyncio.to_thread(extract_zip)

    for name, text in extracted:
        db_file = File(
            archive_id=archive.id,
            filename=name,
            content=text
        )
        session.add(db_file)

    return [{"filename": name, "content": text} for name, text in extracted]