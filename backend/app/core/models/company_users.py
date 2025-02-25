import uuid
from app.core.types.enums.company_user_role import CompanyUserRoleEnum
from sqlmodel import Column, Field, ForeignKeyConstraint, SQLModel, String

class CompanyUserLink(SQLModel, table=True):
    __tablename__ = "company_user_links"
    
    company_id: uuid.UUID = Field(foreign_key="companies.id", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    role: CompanyUserRoleEnum = Field(
        default=CompanyUserRoleEnum.CUSTOMER,
        max_length=25,
        sa_column=Column(String(25)),
    )

    __table_args__ = (
        ForeignKeyConstraint(["company_id"], ["companies.id"], ondelete="CASCADE"),
        ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
    )