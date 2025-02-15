from datetime import datetime
import uuid

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.core.models.folders import Folder
    from app.core.models.knowledge_bases import KnowledgeBase
    from app.core.models.users import User


class File(SQLModel, table=True):
    __tablename__ = "files"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str | None = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    name: str = Field(max_length=255)
    type: str = Field(default="txt")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    creator_id: uuid.UUID = Field(foreign_key="users.id")
    creator: "User" = Relationship(back_populates="files")
    
    parent_id: uuid.UUID = Field(foreign_key="folders.id")
    parent: "Folder" = Relationship(back_populates="files")

    knowledge_base_id: uuid.UUID = Field(nullable=False, foreign_key="knowledge_bases.id")
    knowledge_base: "KnowledgeBase" = Relationship(back_populates="files")

    creator_id: Optional[uuid.UUID] = Field(foreign_key="users.id")
    creator: Optional["User"] = Relationship(back_populates="files")
