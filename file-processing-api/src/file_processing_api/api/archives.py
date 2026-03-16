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

    for archive in archives:
        is_validated = validate_archive(archive)

        if not is_validated:
            continue

        try:
            async with session.begin():  # transaction per archive
                extracted = await process_archive(archive, session)
            results.append({"filename": archive.filename, "files": extracted})
        except ValueError:
            raise HTTPException(400, "Invalid ZIP archive")

    return {"archives": results}


def validate_archive(archive: UploadFile):
    if archive.content_type not in ALLOWED_TYPES or not archive.filename.endswith(".zip"):
        logger.warning("{}: Only ZIP archives allowed", archive.filename)
        return False

    return True