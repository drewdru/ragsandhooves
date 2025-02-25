from datetime import datetime
import uuid

from sqlmodel import Field, ForeignKeyConstraint, Relationship, SQLModel
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.models.companies import Company
    from app.core.models.folders import Folder


class DocumentProvider(SQLModel, table=True):
    __tablename__ = "document_providers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    name: str = Field(max_length=255)
    is_active: bool = True
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    company_id: uuid.UUID = Field(nullable=False, foreign_key="companies.id")
    company: "Company" = Relationship(back_populates="document_providers")

    root_folder_id: uuid.UUID = Field(nullable=False, foreign_key="folders.id")
    root_folder: "Folder" = Relationship(
        back_populates="document_provider",
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['root_folder_id'], ['folders.id'],
            ondelete="CASCADE",
        ),
    )