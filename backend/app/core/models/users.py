import uuid

from app.core.dtos.users import UserBase
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.core.models.items import Item

# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
