import io
import zipfile
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from file_processing_api.db.session import get_session
from file_processing_api.services.data_processor import process_archive
from loguru import logger

logger.add("logs.log", rotation="5 MB", enqueue=True)

router = APIRouter(prefix="/archives", tags=["archives"])
ALLOWED_TYPES = ["application/zip"]


@router.post("/upload")
async def upload_archives(
    archives: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session)
):
    results = []
    invalid_archives = []

    for archive in archives:
        contents = await archive.read()
        is_validated = validate_archive(archive, contents)

        if not is_validated:
            invalid_archives.append(archive.filename)
            continue

        async with session.begin():  # transaction per archive
            extracted = await process_archive(archive.filename, contents, session)
        results.append({"filename": archive.filename, "files": extracted})

    return {
        "archives": results,
        "invalid_archives": invalid_archives
    }


def validate_archive(archive: UploadFile, contents: bytes):
    if archive.content_type not in ALLOWED_TYPES or not archive.filename.endswith(".zip"):
        logger.warning("Invalid archive type or extension: {}", archive.filename)
        return False

    try:
        with zipfile.ZipFile(io.BytesIO(contents)):
            return True
    except zipfile.BadZipFile:
        logger.warning("Bad ZIP file: {}", archive.filename)
        return False