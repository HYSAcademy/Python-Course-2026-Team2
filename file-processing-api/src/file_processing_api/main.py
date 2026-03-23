from pathlib import Path

import joblib
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from file_processing_api.api.archives import router as archives_router
from file_processing_api.db.session import engine as async_engine
from sqlmodel import SQLModel

# Lifespan context manager for startup/shutdown
from contextlib import asynccontextmanager

from file_processing_api.services.tf_idf_indexing import tfidf_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code: create tables or run migrations
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables ensured!")


    if Path("tfidf_vectorizer.pkl").exists():
        tfidf_service.vectorizer = joblib.load("tfidf_vectorizer.pkl")
    
    yield  # This is where the app runs

    # Shutdown code (optional)
    await async_engine.dispose()
    print("Database connection disposed!")

# Create FastAPI app with lifespan
app = FastAPI(lifespan=lifespan)

# Include routers
app.include_router(archives_router)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={"error": str(exc)}
    )