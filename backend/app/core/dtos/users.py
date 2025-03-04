import uuid

from app.core.dtos.token import Token
from pydantic import EmailStr
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    is_staff: bool = False
    is_verified: bool = False
    full_name: str | None = Field(default=None, max_length=255)
    avatar: str | None = Field(default=None)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    google_id: str | None = Field(default=None)


class PrivateUserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_verified: bool = False


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    captcha: str | None = Field(default=None, max_length=4096)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)
    google_id: str | None = Field(default=None)

class UserUpdateVerifyToken(SQLModel):
    verify_token: uuid.UUID

class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID

class UserAuth(UserPublic, Token):
    id: uuid.UUID

class UsersPublicPaginated(SQLModel):
    data: list[UserPublic]
    count: int
