from datetime import datetime
import pyotp
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.models import User
from app.db.database import get_db
from app.core.security import get_password_hash, verify_password
from app.schemas.auth import Signup
from app.schemas.otp import UserBaseSchema, LoginUserSchema, UserRequestSchema


class OTPAuthService:
    @staticmethod
    async def register_user(db: Session, user: UserBaseSchema):
        # Check if user already exists
        existing_user = db.query(User).filter(
            (User.email == user.email.lower()) | (User.username == user.username)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Account already exists'
            )

        # Create new user
        hashed_password = get_password_hash(user.password)
        new_user = User(
            username=user.username,
            email=user.email.lower(),
            password=hashed_password,
            full_name=user.full_name,
            role="user",
            otp_enabled=False,
            otp_verified=False,
            otp_base32=None,
            otp_auth_url=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            'status': 'success',
            'message': 'Registered successfully, please login',
            'user_id': new_user.id
        }

    @staticmethod
    async def login_user(db: Session, payload: LoginUserSchema):
        user = db.query(User).filter(User.email == payload.email.lower()).first()
        if not user or not verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Incorrect Email or Password'
            )

        return {
            'status': 'success',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'otp_enabled': user.otp_enabled,
                'otp_verified': user.otp_verified
            }
        }

    @staticmethod
    async def generate_otp(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )

        # Generate OTP secret
        otp_base32 = pyotp.random_base32()
        otp_auth_url = pyotp.totp.TOTP(otp_base32).provisioning_uri(
            name=user.email, issuer_name="Ticketing API")

        # Update user with OTP details
        user.otp_base32 = otp_base32
        user.otp_auth_url = otp_auth_url
        user.updated_at = datetime.utcnow()
        db.commit()

        return {
            'base32': otp_base32,
            'otpauth_url': otp_auth_url
        }

    @staticmethod
    async def verify_otp(db: Session, user_id: int, token: str):
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.otp_base32:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Token is invalid or user does not exist'
            )

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(token):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid OTP token'
            )

        # Enable OTP for user
        user.otp_enabled = True
        user.otp_verified = True
        user.updated_at = datetime.utcnow()
        db.commit()

        return {
            'otp_verified': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'otp_enabled': user.otp_enabled,
                'otp_verified': user.otp_verified
            }
        }

    @staticmethod
    async def validate_otp(db: Session, user_id: int, token: str):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User does not exist'
            )

        if not user.otp_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='OTP must be verified first'
            )

        totp = pyotp.TOTP(user.otp_base32)
        if not totp.verify(token, valid_window=1):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Invalid OTP token'
            )

        return {'otp_valid': True}

    @staticmethod
    async def disable_otp(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )

        user.otp_enabled = False
        user.otp_verified = False
        user.otp_base32 = None
        user.otp_auth_url = None
        user.updated_at = datetime.utcnow()
        db.commit()

        return {
            'otp_disabled': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'otp_enabled': user.otp_enabled,
                'otp_verified': user.otp_verified
            }
        }
