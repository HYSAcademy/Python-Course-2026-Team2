import io
import zipfile
from typing import List
from fastapi import BackgroundTasks

import aiofiles
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from file_processing_api.db.session import get_session
from loguru import logger

logger.add("logs.log", rotation="5 MB", enqueue=True)

router = APIRouter(prefix="/archives", tags=["archives"])
ALLOWED_TYPES = ["application/zip"]
CHUNK_SIZE = 1024 * 1024

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session)
):
    tasks = [upload_file(file) for file in files ]
    results = await asyncio.gather(*tasks)

async def upload_file(file: UploadFile = File(...)):
    path = f"/tmp/{file.filename}"

    async with aiofiles.open(path, "wb") as temp_file:
        while content := await file.read(CHUNK_SIZE):
            await temp_file.write(content)


    return {"filename": file.filename}

def process_file(path: str):
    pass
