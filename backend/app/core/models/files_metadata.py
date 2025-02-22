import uuid

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.dialects.postgresql import JSONB

if TYPE_CHECKING:
    from app.core.models.files import File


class FileMetadata(SQLModel, table=True):
    __tablename__ = "files_metadata"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    original_id: str | None = Field(max_length=255)
    size: float | None # Gigabytes
    bucket: str | None = Field(max_length=255)
    bucketPath: str | None = Field(max_length=255)
    publicLink: str | None = Field(max_length=255)
    file_name: str | None = Field(max_length=255)
    
    meta: dict = Field(sa_type=JSONB, nullable=False)

    file: Optional["File"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="file_metadata"
    )