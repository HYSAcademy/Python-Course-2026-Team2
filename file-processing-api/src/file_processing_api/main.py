from fastapi import FastAPI
from file_processing_api.api.archives import router as archives_router
from fastapi.responses import JSONResponse
from fastapi import Request


app = FastAPI()

app.include_router(archives_router)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )