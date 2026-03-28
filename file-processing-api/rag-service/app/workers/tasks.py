import asyncio
import os
import joblib
from redis import Redis
from rq import Queue
from file_processing_api.services.tf_idf_indexing import tfidf_service
from file_processing_api.services.file_service import get_all_files
from file_processing_api.services.data_processing import save_vector_parallel
from file_processing_api.db.session import get_session

# Підключення до Redis
# Read Redis host/port from env
REDIS_HOST = os.getenv("REDIS_HOST", "redis")  # default to 'redis' for Docker
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Single Redis connection
redis_conn = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
queue = Queue("default", connection=redis_conn, default_timeout=600)


async def index_files_background():
    """
    Фонова задача для створення TF-IDF індексу та збереження векторів у БД
    """
    session = await get_session().__aenter__()
    try:
        files = await get_all_files(session)
        corpus = [f.content for f in files if f.content]

        # Навчання TF-IDF
        tfidf_service.fit(corpus)
        joblib.dump(tfidf_service.vectorizer, "tfidf_vectorizer.pkl")

        # Збереження векторів у базу
        await asyncio.gather(
            *[
                save_vector_parallel(file.id, tfidf_service.matrix[i])
                for i, file in enumerate(files)
            ]
        )
        await session.commit()
    finally:
        await session.close()


def run_indexing_task():
    """Wrapper for RQ worker — synchronous entry point"""
    asyncio.run(index_files_background())


def enqueue_indexing():
    """Додаємо задачу у Redis Queue"""
    queue.enqueue(run_indexing_task)
