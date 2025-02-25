from datetime import datetime
import uuid

from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.core.models.folders import Folder
    from app.core.models.knowledge_bases import KnowledgeBase
    from app.core.models.users import User
    from app.core.models.recognition_results import RecognitionResult
    from app.core.models.files_metadata import FileMetadata


class File(SQLModel, table=True):
    __tablename__ = "files"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    name: str = Field(max_length=255)
    type: str = Field(default="txt")
    status: str = Field(default="pending")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    creator_id: Optional[uuid.UUID] = Field(foreign_key="users.id")
    creator: Optional["User"] = Relationship(
        back_populates="files_created",
        sa_relationship_kwargs={"foreign_keys": "File.creator_id"},
    )
    
    editor_id: Optional[uuid.UUID] = Field(foreign_key="users.id")
    editor: Optional["User"] = Relationship(
        back_populates="files_edited",
        sa_relationship_kwargs={"foreign_keys": "File.editor_id"},
    )
    
    parent_id: uuid.UUID = Field(foreign_key="folders.id")
    parent: "Folder" = Relationship(
        back_populates="files",
        sa_relationship_kwargs={"foreign_keys": "File.parent_id"},
    )
    
    root_folder_id: uuid.UUID = Field(nullable=False, foreign_key="folders.id")
    root_folder: "Folder" = Relationship(
        back_populates="flat_files",
        sa_relationship_kwargs={"foreign_keys": "File.root_folder_id"},
    )

    knowledge_base_id: uuid.UUID = Field(nullable=False, foreign_key="knowledge_bases.id")
    knowledge_base: "KnowledgeBase" = Relationship(back_populates="files")

    file_metadata_id: Optional[uuid.UUID] = Field(foreign_key="files_metadata.id")
    file_metadata: Optional["FileMetadata"] = Relationship(
        sa_relationship_kwargs={'uselist': False, 'single_parent': True},
        back_populates="file",
        cascade_delete=True,
    )

    recognition_results: Optional["RecognitionResult"] = Relationship(
        back_populates="file",
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['parent_id'], ['folders.id'],
            ondelete="CASCADE",
        ),
    )
