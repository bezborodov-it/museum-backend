from pydantic import BaseModel
from typing import Optional
from pydantic import EmailStr


class UserGet(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserBase(UserGet):
    email: Optional[EmailStr]
    number: str
    name: Optional[str]

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]
