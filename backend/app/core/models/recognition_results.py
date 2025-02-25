from datetime import datetime
import uuid

from app.core.models.recognition_results_metadata import RecognitionResultsMetadata
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.core.models.users import User
    from app.core.models.files import File


class RecognitionResult(SQLModel, table=True):
    __tablename__ = "recognition_results"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    is_active: bool = True
    is_updated: bool = True
    version: int = 0
    status: str = Field(default="pending")
    
    parent_id: Optional[uuid.UUID] = Field(default=None, foreign_key="recognition_results.id")
    parent: Optional["RecognitionResult"] = Relationship(
        sa_relationship_kwargs={"remote_side": "RecognitionResult.id"} ,
        back_populates="children"
    )
    children: list["RecognitionResult"] = Relationship(back_populates="parent")

    file_id: uuid.UUID = Field(foreign_key="files.id")
    file: "File" = Relationship(
        sa_relationship_kwargs={'uselist': False, 'single_parent': True},
        back_populates="recognition_results", 
        cascade_delete=True,
    )
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    creator_id: Optional[uuid.UUID] = Field(foreign_key="users.id")
    creator: Optional["User"] = Relationship(back_populates="recognition_result_created")

    recognition_result_metadata_id: Optional[uuid.UUID] = Field(foreign_key="recognition_results_metadata.id")
    recognition_result_metadata: Optional["RecognitionResultsMetadata"] = Relationship(
        sa_relationship_kwargs={'uselist': False, 'single_parent': True},
        back_populates="recognition_result",
        cascade_delete=True,
    )