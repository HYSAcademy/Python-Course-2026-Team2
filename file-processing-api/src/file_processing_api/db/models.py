from datetime import datetime
from typing import Optional, Dict
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text, JSON, String


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
    file_id: int = Field(foreign_key="file.id", index=True)
    vector: Dict[int, float] = Field(sa_column=Column(JSON, nullable=False))