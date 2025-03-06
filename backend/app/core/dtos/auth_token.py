from datetime import datetime
from sqlmodel import SQLModel

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None

# JSON payload containing csrf token
class CsrfToken(SQLModel):
    token: str
    expire: datetime
