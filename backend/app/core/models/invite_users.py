import uuid
from sqlmodel import Field, SQLModel

class InviteUsersLink(SQLModel, table=True):
    __tablename__ = "invite_users_links"
    
    invite_code: str = Field(foreign_key="invites.code", primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
