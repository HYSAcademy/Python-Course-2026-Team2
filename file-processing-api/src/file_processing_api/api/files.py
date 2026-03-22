import asyncio
import uuid
from typing import List

import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends
from loguru import logger
from rq import Queue
from sklearn.feature_extraction.text import TfidfVectorizer

from file_processing_api.redis_client import redis_connection
from file_processing_api.services.data_processing import process_file
from file_processing_api.services.file_validation import FileValidationService

router = APIRouter(prefix="/files", tags=["files"])
CHUNK_SIZE = 1024 * 1024

q = Queue(connection=redis_connection)
semaphore = asyncio.Semaphore(25)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    logger.info(f"START")

    corpus = await asyncio.gather(*[upload_file(file) for file in files])



async def upload_file(file: UploadFile):
    await FileValidationService.validate(file)

    path = f"/storage/files/{uuid.uuid4()}_{file.filename}"
    chunks = []

    async with semaphore:
        async with aiofiles.open(path, "wb") as f:
            while content := await file.read(CHUNK_SIZE):
                await f.write(content)
                chunks.append(content.decode("utf-8", errors="ignore"))

    return " ".join(chunks)


