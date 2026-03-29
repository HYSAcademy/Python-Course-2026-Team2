from datetime import datetime
from typing import Optional, List

from pgvector.sqlalchemy import Vector
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Text, UniqueConstraint


class Archive(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class File(SQLModel, table=True):
    __tablename__ = "file"

    id: Optional[int] = Field(default=None, primary_key=True)
    archive_id: int = Field(foreign_key="archive.id", index=True)
    filename: str = Field(index=True, max_length=255, nullable=False)
    path: str = Field(index=True, max_length=1024, nullable=False)

    chunks: List["FileChunk"] = Relationship(back_populates="file")


class FileChunk(SQLModel, table=True):
    __tablename__ = "file_chunk"
    __table_args__ = (
        UniqueConstraint("file_id", "chunk_index"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    file_id: int = Field(foreign_key="file.id", index=True)

    chunk_index: int = Field(index=True)
    text: str = Field(sa_column=Column(Text))
    vector: list[float] = Field(sa_column=Column(Vector(1536), nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    file: Optional["File"] = Relationship(back_populates="chunks")