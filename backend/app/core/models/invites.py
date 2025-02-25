import uuid

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Column, Field, ForeignKeyConstraint, SQLModel, Relationship, String

from app.core.types.enums.company_user_role import CompanyUserRoleEnum
from app.core.models.invite_users import InviteUsersLink

if TYPE_CHECKING:
    from app.core.models.companies import Company
    from app.core.models.knowledge_bases import KnowledgeBase
    from app.core.models.users import User


class Invite(SQLModel, table=True):
    __tablename__ = "invites"
    
    code: str = Field(primary_key=True)
    title: str | None = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    role: CompanyUserRoleEnum = Field(
        default=CompanyUserRoleEnum.CUSTOMER,
        max_length=25,
        sa_column=Column(String(25)),
    )
    expires_at: Optional[datetime]
    max_users: Optional[int]
    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})

    company_id: uuid.UUID = Field(foreign_key="companies.id")
    company: "Company" = Relationship(back_populates="invites")

    knowledge_base_id: Optional[uuid.UUID] = Field(foreign_key="knowledge_bases.id")
    knowledge_base: Optional["KnowledgeBase"] = Relationship(back_populates="invites")

    users: List["User"] = Relationship(
        back_populates="invites",
        link_model=InviteUsersLink,
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ['company_id'], ['companies.id'],
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ['knowledge_base_id'], ['knowledge_bases.id'],
            ondelete="CASCADE",
        ),
    )
