from datetime import datetime

from sqlmodel import Field, SQLModel

class Tier(SQLModel, table=True):
    __tablename__ = "tiers"
    
    id: str = Field(primary_key=True)
    title: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=255)
    
    max_files: int = Field(default=10)
    max_tokens_per_day: int = Field(default=1000)
        
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column_kwargs={"onupdate": datetime.now})
