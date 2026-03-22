import asyncio
import uuid
import aiofiles
from typing import List
from fastapi import APIRouter, UploadFile, File
from file_processing_api.services.tf_idf_indexing import TFIDFService
from file_processing_api.services.file_validation import FileValidationService

tfidf_service = TFIDFService()

CHUNK_SIZE = 1024 * 1024
semaphore = asyncio.Semaphore(25)

router = APIRouter(prefix="/files", tags=["files"])

@router.post("/index")
async def index_files(files: List[UploadFile] = File(...)):
    corpus = await asyncio.gather(*[upload_file(file) for file in files])

    tfidf_service.fit(corpus)


async def upload_file(file: UploadFile):
    await FileValidationService.validate(file)

    path = f"/storage/files/{uuid.uuid4()}_{file.filename}"
    chunks = []

    async with semaphore:
        async with aiofiles.open(path, "wb") as f:
            while content := await file.read(CHUNK_SIZE):
                await f.write(content)
                chunks.append(content.decode("utf-8", errors="ignore"))

    return "".join(chunks)


