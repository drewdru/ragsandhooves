from datetime import datetime
import uuid

from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional
from sqlalchemy.dialects.postgresql import JSONB


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
    original_id: str | None = Field(default=None, max_length=255)
    meta: dict = Field(sa_type=JSONB, nullable=False)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    knowledge_base_id: uuid.UUID = Field(nullable=False, foreign_key="knowledge_bases.id")
    knowledge_base: "KnowledgeBase" = Relationship(back_populates="folders")

    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="folders.id")
    parent: Optional["Folder"] = Relationship(
        sa_relationship_kwargs={"remote_side": "Folder.id"} ,
        back_populates="sub_folders"
    )
    sub_folders: list["Folder"] = Relationship(back_populates="parent")

    document_provider: Optional["DocumentProvider"] = Relationship(
        sa_relationship_kwargs={'uselist': False, 'single_parent': True},
        back_populates="root_folder",
    )
    files: list["File"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"foreign_keys": "File.parent_id"},
    )
    flat_files: list["File"] = Relationship(
        back_populates="root_folder",
        sa_relationship_kwargs={"foreign_keys": "File.root_folder_id"},
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['parent_id'], ['folders.id'],
            ondelete="CASCADE",
        ),
    )