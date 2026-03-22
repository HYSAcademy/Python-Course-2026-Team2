import asyncio
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession

from file_processing_api.db.session import get_session
from file_processing_api.services.data_processing import extract_files, process_archive, upload_file
from file_processing_api.services.tf_idf_indexing import TFIDFService
from file_processing_api.services.file_validation import FileValidationService

tfidf_service = TFIDFService()

router = APIRouter(prefix="/archives", tags=["archives"])

@router.post("/upload")
async def upload_archives(
    archives: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session)
):
    results = []

    for archive in archives:
        await FileValidationService.validate(archive)
        contents = await archive.read()

        async with session.begin():
            extracted = await process_archive(archive.filename, contents, session)
        results.append({"filename": archive.filename, "files": extracted})

    return {
        "archives": results,
    }


@router.post("/index")
async def index_archive(archive: UploadFile):
    await FileValidationService.validate(archive)
    logger.info("INDEXING STARTED")

    contents = await archive.read()

    files = extract_files(contents)
    corpus = await asyncio.gather(*[upload_file(filename, text) for filename, text in files])

    tfidf_service.fit(corpus)


