import asyncio
from typing import List

import joblib
from fastapi import APIRouter, UploadFile, File, Depends, Query
from loguru import logger
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from file_processing_api.db.session import get_session
from file_processing_api.services.data_processing import extract_files, process_archive, upload_file, save_vector
from file_processing_api.services.file_service import get_all_files, get_all_vectors
from file_processing_api.services.tf_idf_indexing import TFIDFService, tfidf_service
from file_processing_api.services.file_validation import FileValidationService


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
async def index(session: AsyncSession = Depends(get_session)):
    files = await get_all_files(session)
    corpus = [file.content for file in files if file.content]
    tfidf_service.fit(corpus)
    matrix = tfidf_service.matrix

    joblib.dump(tfidf_service.vectorizer, "tfidf_vectorizer.pkl")

    await asyncio.gather(*[
        save_vector(file.id, matrix[i], session) for i, file in enumerate(files)
    ])

    await session.commit()

    return JSONResponse(status_code=200, content={"message": "ok"})

@router.get("/search")
async def search_query(
    query: str = Query(...),
    top_k: int = Query(5),
    session: AsyncSession = Depends(get_session)
):
    pass



