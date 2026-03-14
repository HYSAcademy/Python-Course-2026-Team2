from fastapi import FastAPI
from sqlmodel import SQLModel
from db.database import engine


SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}