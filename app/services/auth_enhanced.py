from fastapi import HTTPException, Depends, status, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.models import User
from app.db.database import get_db
from app.core.security import verify_password, get_user_token, get_token_payload
from app.core.security import get_password_hash
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup
from app.services.login_tracking import LoginTrackingService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthEnhancedService:
    @staticmethod
    async def login_with_tracking(
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
        request: Request = None
    ):
        """
        Enhanced login method that tracks login attempts by role
        """
        return await LoginTrackingService.login_with_tracking(
            user_credentials, db, request
        )

    @staticmethod
    async def signup(db: Session, user: Signup):
        """
        User signup method
        """
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
        role = getattr(user, "role", "user")
        db_user = User(id=None, role=role, **user.model_dump(exclude={"role"}))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def get_refresh_token(token, db):
        """
        Get refresh token
        """
        payload = get_token_payload(token)
        user_id = payload.get('id', None)
        if not user_id:
            raise ResponseHandler.invalid_token('refresh')

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.invalid_token('refresh')

        return await get_user_token(id=user.id, refresh_token=token)
