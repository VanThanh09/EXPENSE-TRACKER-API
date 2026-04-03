from datetime import datetime

from pydantic import BaseModel, model_validator
from typing import Optional, List


# -----------------------auth-----------------------
class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires: float


class TokenData(BaseModel):
    email: Optional[str] = None


# -----------------------user-----------------------
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    confirm_password: str
    avatar: Optional[str] = None

    def get_avatar(self):
        return self.avatar if self.avatar else "https://res.cloudinary.com/drzc4fmxb/image/upload/v1733907010/xvethjfe9cycrroqi7po.jpg"

    @model_validator(mode="after")
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    avatar: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool
    avatar: str

    class Config:
        from_attributes = True


# -----------------------blog-----------------------
class Author(BaseModel):
    name: str
    avatar: str


class Image(BaseModel):
    url: str


class BlogList(BaseModel):
    title: Optional[str] = None
    content: str
    created_at: datetime
    author: Author
    images: Optional[List[Image]] = None

    class Config:
        from_attributes = True


class BlogPost(BaseModel):
    title: Optional[str] = None
    content: str
    is_published: bool

    images: Optional[List[Image]] = None


class Blog(BaseModel):
    id: int
    title: Optional[str] = None
    content: str
    is_published: bool
    created_at: datetime
    author: Author
    images: Optional[List[Image]] = None
