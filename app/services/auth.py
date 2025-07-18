from fastapi import HTTPException, Depends, status, Request
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.models import User
from app.models.user_session import UserSession
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
import secrets
import os
from app.db.database import get_db
from app.core.security import verify_password, get_user_token, get_token_payload
from app.core.security import get_password_hash
from app.utils.responses import ResponseHandler
from app.schemas.auth import Signup
from datetime import datetime
import uuid


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    @staticmethod
    async def login(user_credentials: OAuth2PasswordRequestForm, db: Session, request: Request):
    #async def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db),request: Request = None):
        user = db.query(User).filter(User.username == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

        tokens = await get_user_token(id=user.id)
        if not tokens or not isinstance(tokens, dict):
            raise HTTPException(status_code=500, detail="Token generation failed")
        
        # Save user session
        session = UserSession(
            user_id=user.id,
            session_token=tokens["access_token"],
            ip_address = request.client.host,
            user_agent=request.headers.get("user-agent"),
            last_activity=datetime.utcnow(),
            is_active=True
        )
        db.add(session)
        db.commit()

        return {
            **tokens,
            "role": user.role
        }

    @staticmethod
    async def signup(db: Session, user: Signup):
        hashed_password = get_password_hash(user.password)
        user.password = hashed_password
<<<<<<< HEAD
=======
        #db_user = User(id=None, **user.model_dump())
>>>>>>> b600bb7 (fifth commit)
        role = getattr(user, "role", "user")
        db_user = User(id=None, role=role, **user.model_dump(exclude={"role"}))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return ResponseHandler.create_success(db_user.username, db_user.id, db_user)

    @staticmethod
    async def get_refresh_token(token, db):
        payload = get_token_payload(token)
        user_id = payload.get('id', None)
        if not user_id:
            raise ResponseHandler.invalid_token('refresh')

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.invalid_token('refresh')

        return await get_user_token(id=user.id, refresh_token=token)
