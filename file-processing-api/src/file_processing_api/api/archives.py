import asyncio
from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from loguru import logger
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from file_processing_api.db.session import get_session
from file_processing_api.services.data_processing import extract_files, process_archive, upload_file, save_vector
from file_processing_api.services.file_service import get_files_by_archive_id
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


@router.post("/index/{archive_id}")
async def index_archive(archive_id: int, session: AsyncSession = Depends(get_session)):
    files = await get_files_by_archive_id(archive_id, session)
    corpus = [file.content for file in files if file.content]
    tfidf_service.fit(corpus)
    matrix = tfidf_service.matrix

    await asyncio.gather(*[
        save_vector(file.id, matrix[i], session) for i, file in enumerate(files)
    ])

    await session.commit()
    # vocab = tfidf_service.vectorizer.get_feature_names_out()
    # logger.info(f"58 WORD {vocab[58]}")
    # logger.info(f"69 WORD {vocab[69]}") // Save for presentation

    return JSONResponse(status_code=200, content={"message": "ok"})



