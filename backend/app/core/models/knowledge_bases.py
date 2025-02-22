from datetime import datetime
import uuid

from app.core.models.customers_knowledge_bases import CustomerKnowledgeBaseLink
from app.core.models.company_knowledge_bases import CompanyKnowledgeBaseLink
from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.core.models.companies import Company
    from app.core.models.users import User
    from app.core.models.folders import Folder
    from app.core.models.files import File
    from app.core.models.invites import Invite
    from app.core.models.agents_parameters import AgentsParameters


class KnowledgeBase(SQLModel, table=True):
    __tablename__ = "knowledge_bases"
    
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    companies: List["Company"] = Relationship(
        back_populates="knowledge_bases",
        link_model=CompanyKnowledgeBaseLink,
        cascade_delete=True,
    )
    customers: List["User"] = Relationship(
        back_populates="knowledge_bases",
        link_model=CustomerKnowledgeBaseLink,
        cascade_delete=True,
    )
    
    folders: list["Folder"] = Relationship(back_populates="knowledge_base", cascade_delete=True)
    files: list["File"] = Relationship(back_populates="knowledge_base", cascade_delete=True)

    invites: List["Invite"] = Relationship(
        back_populates="company",
        cascade_delete=True,
    )

    # Use to save parameters of agents like Question Extractions for every particular Knowledge Base
    agents_parameters: List["AgentsParameters"] = Relationship(
        back_populates="knowledge_base", 
        cascade_delete=True
    )