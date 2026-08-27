from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Literal
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class UserLogin(UserCreate):
    pass

class PostBase(BaseModel):
    title: str
    content: str
    is_published: bool

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    model_config = ConfigDict(from_attributes=True)

class Vote(BaseModel):
    post_id: int
    dir: Literal[0,1]

