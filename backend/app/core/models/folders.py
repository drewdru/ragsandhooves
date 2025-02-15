from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from app.core.models.files import File
    from app.core.models.document_providers import DocumentProvider
    from app.core.models.knowledge_bases import KnowledgeBase


class Folder(SQLModel, table=True):
    __tablename__ = "folders"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(default=None, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    name: str = Field(max_length=255)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    knowledge_base_id: uuid.UUID = Field(nullable=False, foreign_key="knowledge_bases.id")
    knowledge_base: "KnowledgeBase" = Relationship(back_populates="folders")

    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="folders.id")
    parent: Optional["Folder"] = Relationship(back_populates="files")
    sub_folders: list["Folder"] = Relationship(back_populates="parent")

    document_provider: Optional["DocumentProvider"] = Relationship(
        sa_relationship_kwargs={'uselist': False},
        back_populates="root_folder"
    )
    files: list["File"] = Relationship(
        back_populates="parent",
        cascade_delete=True,
    )
