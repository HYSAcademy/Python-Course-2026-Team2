import io
import os
import zipfile
import magic
from fastapi import UploadFile, HTTPException

MAX_FILE_SIZE = 10 * 1024 * 1024
ALLOWED_ZIP_MIMES = ["application/zip", "application/x-zip-compressed",  "application/octet-stream"]


class FileValidationService:

    @staticmethod
    async def validate(file: UploadFile) -> None:
        await FileValidationService. _validate_extension(file)
        await FileValidationService._validate_mime(file)
        await FileValidationService._validate_archive(file)

    @staticmethod
    async def _validate_extension(file: UploadFile):
        _, ext = os.path.splitext(file.filename)
        if ext.lower() != ".zip":
            raise HTTPException(400, "Only .zip files allowed")

    @staticmethod
    async def _validate_mime(file: UploadFile):
        await file.seek(0)
        header = await file.read(2048)
        await file.seek(0)
        mime = magic.from_buffer(header, mime=True)

        if mime not in ALLOWED_ZIP_MIMES:
            raise HTTPException(status_code=400, detail=f"Invalid MIME type: {mime}")

    @staticmethod
    async def _validate_archive(file: UploadFile):
        content = await file.read()
        await file.seek(0)

        try:
            with zipfile.ZipFile(io.BytesIO(content)) as zf:
                files = [info for info in zf.infolist() if not info.is_dir()]

                if not files:
                    raise HTTPException(status_code=400, detail="Empty ZIP archive")

                for info in files:
                    if info.filename.startswith("/") or ".." in info.filename:
                        raise HTTPException(status_code=400, detail="Unsafe file path in ZIP")

                    if not info.filename.lower().endswith(".txt"):
                        raise HTTPException(status_code=400, detail="ZIP must contain only .txt files")

                    if info.file_size > MAX_FILE_SIZE:
                        raise HTTPException(status_code=400, detail=f"{info.filename} exceeds max file size")

        except zipfile.BadZipFile:
            raise HTTPException(status_code=400, detail="Invalid ZIP archive")