# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class EmailSchema(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    # 移除 username
    email: EmailStr
    password: str
    code: str

class UserInDB(BaseModel):
    id: int
    # 移除 username
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # 将 subject 从 username 改为 email
    email: Optional[str] = None