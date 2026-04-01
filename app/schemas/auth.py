from pydantic import BaseModel
from typing import Optional

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires: int


class TokenData(BaseModel):
    email: Optional[str] = None