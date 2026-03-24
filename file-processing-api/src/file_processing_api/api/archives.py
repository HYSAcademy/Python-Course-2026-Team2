import asyncio
from typing import List

import joblib
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from file_processing_api.db.session import get_session
from file_processing_api.services.data_processing import (
    process_archive,
    save_vector_parallel,
)
from file_processing_api.services.file_service import get_all_files, get_all_vectors
from file_processing_api.services.tf_idf_indexing import tfidf_service
from file_processing_api.services.file_validation import FileValidationService


router = APIRouter(prefix="/archives", tags=["archives"])


@router.post("/upload")
async def upload_archives(
    archives: List[UploadFile] = File(...), session: AsyncSession = Depends(get_session)
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

    await asyncio.gather(
        *[save_vector_parallel(file.id, matrix[i]) for i, file in enumerate(files)]
    )

    return {"message": "ok"}


@router.get("/search")
async def search_query(
    query: str = Query(...),
    top_k: int = Query(5),
    session: AsyncSession = Depends(get_session),
):
    vectors = await get_all_vectors(session)

    if not vectors:
        return {"results": [], "message": "No vectors found"}

    query_vec = tfidf_service.transform([query])

    similarities = tfidf_service.get_similarities(query_vec, vectors)
    top_indices = similarities.argsort()[::-1][:top_k]

    results = [
        {"file_id": vectors[i].file_id, "score": float(similarities[i])}
        for i in top_indices
        if float(similarities[i])
    ]

    return {"results": results}


@router.post("/index/background")
async def index_background():
    """
    Запускаємо TF-IDF індексацію в фоні через Redis Queue
    """
    from file_processing_api.workers.tasks import enqueue_indexing

    enqueue_indexing()
    return {"message": "TF-IDF indexing started in background"}
