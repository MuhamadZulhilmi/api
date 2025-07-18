from pydantic import BaseModel, EmailStr
from datetime import datetime
<<<<<<< HEAD
from typing import List, Optional
=======
from typing import List
from typing import Optional

>>>>>>> b600bb7 (fifth commit)
# Base
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


class Signup(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    role: Optional[str] = "user"

    class Config(BaseConfig):
        pass


class UserOut(BaseModel):
    message: str
    data: UserBase

    class Config(BaseConfig):
        pass


# Token
class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
