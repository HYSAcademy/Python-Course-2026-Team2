import asyncio
import datetime
from typing import List

import joblib
from fastapi import APIRouter, UploadFile, File, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession


from services.api_service.app.db import get_session_factory, get_session
from services.api_service.app.services.data_processing import handle_archive


router = APIRouter(prefix="/archives", tags=["archives"])


@router.post("/upload")
async def upload_archives(
    archives: List[UploadFile] = File(...), session_factory=Depends(get_session_factory)
):
    start_at = datetime.datetime.now()
    tasks = [handle_archive(archive, session_factory) for archive in archives]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    processed = []
    for archive, result in zip(archives, results):
        if isinstance(result, Exception):
            processed.append(
                {"filename": archive.filename, "status": 500, "error": str(result)}
            )
        else:
            processed.append({"filename": archive.filename, "status": 200})
            publish_message("files_uploaded", {"archive_id": archive.id})

    return {
        "archives": processed,
        "process_time": (datetime.datetime.now() - start_at).total_seconds(),
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
    from file_processing_api.workers.tasks import enqueue_indexing

    enqueue_indexing()
    return {"message": "TF-IDF indexing started in background"}
