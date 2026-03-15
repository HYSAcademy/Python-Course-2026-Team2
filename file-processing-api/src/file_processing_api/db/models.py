from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, Text


class Archive(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)


class File(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    archive_id: int = Field(foreign_key="archive.id")
    filename: str
    content: str = Field(sa_column=Column(Text))