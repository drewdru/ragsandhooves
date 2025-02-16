import uuid

from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, List, Optional

from app.core.models.company_knowledge_bases import CompanyKnowledgeBaseLink
from app.core.models.company_users import CompanyUserLink

if TYPE_CHECKING:
    from app.core.models.users import User
    from app.core.models.knowledge_bases import KnowledgeBase
    from app.core.models.document_providers import DocumentProvider
    from app.core.models.invites import Invite


class Company(SQLModel, table=True):
    __tablename__ = "companies"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    tier: str= Field(default="trial")
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    owner_id: uuid.UUID = Field(
        foreign_key="users.id", nullable=False, ondelete="CASCADE"
    )
    owner: Optional["User"] = Relationship(back_populates="companies")
    
    users: List["User"] = Relationship(
        back_populates="companies",
        link_model=CompanyUserLink,
        cascade_delete=True,
    )
    knowledge_bases: List["KnowledgeBase"] = Relationship(
        back_populates="companies",
        link_model=CompanyKnowledgeBaseLink,
        cascade_delete=True,
    )
    document_providers: list["DocumentProvider"] = Relationship(
        back_populates="company",
        cascade_delete=True,
    )

    invites: List["Invite"] = Relationship(
        back_populates="company",
        cascade_delete=True,
    )
