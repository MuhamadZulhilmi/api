from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from app.models.user_session import UserSession
from app.models.models import User
import uuid


class OnlineStatusService:
    @staticmethod
    async def create_session(
        user_id: int,
        db: Session,
        request: Request = None
    ) -> str:
        """Create a new user session and return session token"""
        session_token = str(uuid.uuid4())
        
        ip_address = request.client.host if request else None
        user_agent = request.headers.get("user-agent") if request else None
        
        # Deactivate any existing sessions for this user
        existing_sessions = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True
        ).all()
        
        for session in existing_sessions:
            session.is_active = False
        
        # Create new session
        new_session = UserSession(
            user_id=user_id,
            session_token=session_token,
            ip_address=ip_address,
            user_agent=user_agent,
            last_activity=datetime.utcnow(),
            is_active=True
        )
        
        db.add(new_session)
        db.commit()
        
        return session_token
    
    @staticmethod
    async def update_last_activity(
        session_token: str,
        db: Session
    ):
        """Update last activity for a session"""
        session = db.query(UserSession).filter(
            UserSession.session_token == session_token,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.last_activity = datetime.utcnow()
            db.commit()
    
    @staticmethod
    async def logout_session(
        session_token: str,
        db: Session
    ):
        """Logout a specific session"""
        session = db.query(UserSession).filter(
            UserSession.session_token == session_token,
            UserSession.is_active == True
        ).first()
        
        if session:
            session.is_active = False
            db.commit()
    
    @staticmethod
    async def get_online_users_by_role(
        db: Session,
        role: str = None,
        timeout_minutes: int = 30
    ):
        """Get currently online users by role"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        query = db.query(User).join(UserSession).filter(
            UserSession.is_active == True,
            UserSession.last_activity >= cutoff_time
        )
        
        if role:
            query = query.filter(User.role == role)
        
        return query.all()
    
    @staticmethod
    async def get_online_count_by_role(
        db: Session,
        timeout_minutes: int = 30
    ):
        """Get count of online users grouped by role"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        return db.query(
            User.role,
            func.count(User.id).label('online_count')
        ).join(UserSession).filter(
            UserSession.is_active == True,
            UserSession.last_activity >= cutoff_time
        ).group_by(User.role).all()
    
    @staticmethod
    async def get_user_sessions(
        user_id: int,
        db: Session
    ):
        """Get all active sessions for a user"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=30)
        
        return db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.last_activity >= cutoff_time
        ).all()
    
    @staticmethod
    async def cleanup_expired_sessions(
        db: Session,
        timeout_minutes: int = 60
    ):
        """Clean up expired sessions"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        expired_sessions = db.query(UserSession).filter(
            UserSession.last_activity < cutoff_time,
            UserSession.is_active == True
        ).all()
        
        for session in expired_sessions:
            session.is_active = False
        
        db.commit()
        
        return len(expired_sessions)
    
    @staticmethod
    async def is_user_online(
        user_id: int,
        db: Session,
        timeout_minutes: int = 30
    ) -> bool:
        """Check if a specific user is online"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        session = db.query(UserSession).filter(
            UserSession.user_id == user_id,
            UserSession.is_active == True,
            UserSession.last_activity >= cutoff_time
        ).first()
        
        return session is not None
    
    @staticmethod
    async def get_total_online_users(
        db: Session,
        timeout_minutes: int = 30
    ) -> int:
        """Get total count of online users"""
        cutoff_time = datetime.utcnow() - timedelta(minutes=timeout_minutes)
        
        return db.query(User).join(UserSession).filter(
            UserSession.is_active == True,
            UserSession.last_activity >= cutoff_time
        ).count()
