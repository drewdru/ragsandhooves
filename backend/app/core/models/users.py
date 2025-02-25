import uuid

from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, List

from app.core.models.company_users import CompanyUserLink
from app.core.models.customers_knowledge_bases import CustomerKnowledgeBaseLink
from app.core.models.invite_users import InviteUsersLink

if TYPE_CHECKING:
    from app.core.models.companies import Company
    from app.core.models.knowledge_bases import KnowledgeBase
    from app.core.models.invites import Invite
    from app.core.models.files import File
    from app.core.models.recognition_results import RecognitionResult


# Database model, database table inferred from class name
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
    
    companies: List["Company"] = Relationship(
        back_populates="users",
        link_model=CompanyUserLink,
    )
    knowledge_bases: List["KnowledgeBase"] = Relationship(
        back_populates="customers",
        link_model=CustomerKnowledgeBaseLink,
    )
    
    invites: List["Invite"] = Relationship(
        back_populates="users",
        link_model=InviteUsersLink,
    )
    
    files_created: List["File"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "File.creator_id"},
    )

    files_edited: List["File"] = Relationship(
        back_populates="editor",
        sa_relationship_kwargs={"foreign_keys": "File.editor_id"},
    )

    recognition_result_created: List["RecognitionResult"] = Relationship(
        back_populates="creator",
        sa_relationship_kwargs={"foreign_keys": "RecognitionResult.creator_id"},
    )
