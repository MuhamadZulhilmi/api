from pydantic import BaseModel , EmailStr
from typing import List
from datetime import datetime
class BaseConfig:
    from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: str
    password: str
    role: str
    is_active: bool
    created_at: datetime

    class Config(BaseConfig):
        pass


class UserCreate(BaseModel):
    full_name: str
    username: str
    email: str
    password: str

    class Config(BaseConfig):
        pass


class UserUpdate(UserCreate):
    pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


class UsersOut(BaseModel):
    message: str
    data: List[UserBase]

    class Config(BaseConfig):
        pass


class UserOutDelete(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass
