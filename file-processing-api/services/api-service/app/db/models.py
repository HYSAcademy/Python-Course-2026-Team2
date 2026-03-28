from datetime import datetime
from typing import Optional

from pgvector.sqlalchemy import Vector
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, String


class Archive(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    archive_id: int = Field(foreign_key="archive.id")
    filename: str = Field(sa_column=Column(String, nullable=False))
    path: str = Field(sa_column=Column(String, nullable=False))
    content: str = Field(sa_column=Column(Text))


class FileVector(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_id: int = Field(foreign_key="file.id", index=True, unique=True)
    vector: list[float] = Field(sa_column=Column(Vector(1536), nullable=False))