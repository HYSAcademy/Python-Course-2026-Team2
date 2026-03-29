from fastapi import FastAPI
from app.api.routes import router
from services.rag_service.app.listeners.file_events_listener import start_listener

if __name__ == "__main__":
    start_listener()

app = FastAPI(title="RAG Service")

app.include_router(router, prefix="/rag")

@app.get("/health")
def health():
    return {"status": "ok"}