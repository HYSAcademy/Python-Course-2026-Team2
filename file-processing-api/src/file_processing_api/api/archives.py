from typing import List
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from file_processing_api.db.session import get_session
from file_processing_api.services.data_processor import process_archive

router = APIRouter(prefix="/archives", tags=["archives"])
MAX_SIZE = 5 * 1024 * 1024
ALLOWED_TYPES = ["application/zip"]


@router.post("/upload")
async def upload_archives(
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session)
):
    results = []

    for file in files:
        if file.content_type not in ALLOWED_TYPES or not file.filename.endswith(".zip"):
            raise HTTPException(400, "Only ZIP archives allowed")
        contents = await file.read()
        if len(contents) > MAX_SIZE:
            raise HTTPException(400, "File too large")

        try:
            async with session.begin():  # transaction per archive
                extracted = await process_archive(file.filename, contents, session)
            results.append({"filename": file.filename, "files": extracted})
        except ValueError:
            raise HTTPException(400, "Invalid ZIP archive")

    return {"archives": results}