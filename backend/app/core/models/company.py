import uuid

from app.core.dtos.users import UserBase
from pydantic import EmailStr
from sqlmodel import Field, Relationship
from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from app.core.models.items import Item

class company(UserBase, table=True):
    company_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    prompt_qa: str | None = Field(default=None, max_length=2550)