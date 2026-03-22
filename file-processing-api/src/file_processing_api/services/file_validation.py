import zipfile
from fastapi import UploadFile


ALLOWED_EXTENSIONS = ["txt"]
MAX_FILE_SIZE = 10 * 1024 * 1024


class FileValidationService:

    @staticmethod
    async def validate(file: UploadFile) -> None:
        await FileValidationService._validate_extension(file)
        await FileValidationService._validate_size(file)

    @staticmethod
    async def _validate_extension(file: UploadFile):
        if not file.filename:
            raise ValueError("File has no name")

        ext = file.filename.split(".")[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError("Invalid file extension")

    @staticmethod
    async def _validate_size(file: UploadFile):
        size = 0

        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_SIZE:
                raise ValueError("The file is too large")

        await file.seek(0)