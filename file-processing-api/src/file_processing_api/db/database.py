import os
from sqlmodel import create_engine

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/postgres"
)

engine = create_engine(DATABASE_URL, echo=True)