import uuid
from sqlmodel import Field, SQLModel

class CompanyKnowledgeBaseLink(SQLModel, table=True):
    __tablename__ = "company_knowledge_base_links"
    
    company_id: uuid.UUID = Field(foreign_key="companies.id", primary_key=True)
    knowledge_base_id: uuid.UUID = Field(foreign_key="knowledge_bases.id", primary_key=True)
