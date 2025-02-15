import uuid
from sqlmodel import Field, SQLModel

class CustomerKnowledgeBaseLink(SQLModel, table=True):
    __tablename__ = "customer_knowledge_base_links"
    
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    knowledge_base_id: uuid.UUID = Field(foreign_key="knowledge_bases.id", primary_key=True)
