import io
import zipfile
import pytest
from httpx import AsyncClient, ASGITransport

from file_processing_api.main import app


def create_zip_file():
    buffer = io.BytesIO()

    with zipfile.ZipFile(buffer, "w") as z:
        z.writestr("test.txt", "hello world")

    buffer.seek(0)
    return buffer


@pytest.mark.asyncio
async def test_upload_archive_success():
    zip_file = create_zip_file()

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/archives/upload",
            files={"archives": ("test.zip", zip_file, "application/zip")},
        )

    assert response.status_code == 200

    data = response.json()
    assert len(data["archives"]) == 1
    assert data["archives"][0]["files"][0]["content"] == "hello world"


@pytest.mark.asyncio
async def test_invalid_zip():
    invalid_file = io.BytesIO(b"invalid")

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "/archives/upload",
            files={"archives": ("bad.zip", invalid_file, "application/zip")},
        )

    data = response.json()
    assert "bad.zip" in data["invalid_archives"]
