from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBaseSchema(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


class UserRequestSchema(BaseModel):
    user_id: int
    token: Optional[str] = None

    class Config:
        from_attributes = True


class OTPResponseSchema(BaseModel):
    base32: str
    otpauth_url: str

    class Config:
        from_attributes = True


class OTPVerifyResponseSchema(BaseModel):
    otp_verified: bool
    user: dict

    class Config:
        from_attributes = True


class OTPDisableResponseSchema(BaseModel):
    otp_disabled: bool
    user: dict

    class Config:
        from_attributes = True
