<<<<<<< HEAD
from fastapi import APIRouter, Depends, Query, status
=======
from fastapi import APIRouter, Depends, Query, status, Request
>>>>>>> b600bb7 (fifth commit)
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.services.online_status import OnlineStatusService

router = APIRouter(tags=["Online Status"], prefix="/online-status")


@router.get("/online-users", status_code=status.HTTP_200_OK)
async def get_online_users(
    role: Optional[str] = Query(None, description="Filter by user role"),
    timeout_minutes: int = Query(30, description="Timeout in minutes for considering user online"),
    db: Session = Depends(get_db)
):
    """
    Get currently online users filtered by role
    """
    return await OnlineStatusService.get_online_users_by_role(
        db, role, timeout_minutes
    )


@router.get("/online-count", status_code=status.HTTP_200_OK)
async def get_online_count(
    timeout_minutes: int = Query(30, description="Timeout in minutes for considering user online"),
    db: Session = Depends(get_db)
):
    """
    Get count of online users grouped by role
    """
    return await OnlineStatusService.get_online_count_by_role(db, timeout_minutes)


@router.get("/user/{user_id}/sessions", status_code=status.HTTP_200_OK)
async def get_user_sessions(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all active sessions for a specific user
    """
    return await OnlineStatusService.get_user_sessions(user_id, db)


@router.post("/create-session", status_code=status.HTTP_201_CREATED)
async def create_session(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    Create a new user session
    """
    return await OnlineStatusService.create_session(user_id, db, request)


@router.post("/logout/{session_token}", status_code=status.HTTP_200_OK)
async def logout_session(
    session_token: str,
    db: Session = Depends(get_db)
):
    """
    Logout a specific session
    """
    await OnlineStatusService.logout_session(session_token, db)
    return {"message": "Session logged out successfully"}


@router.get("/is-online/{user_id}", status_code=status.HTTP_200_OK)
async def is_user_online(
    user_id: int,
    timeout_minutes: int = Query(30, description="Timeout in minutes for considering user online"),
    db: Session = Depends(get_db)
):
    """
    Check if a specific user is online
    """
    is_online = await OnlineStatusService.is_user_online(user_id, db, timeout_minutes)
    return {"user_id": user_id, "is_online": is_online}


@router.get("/total-online", status_code=status.HTTP_200_OK)
async def get_total_online(
    timeout_minutes: int = Query(30, description="Timeout in minutes for considering user online"),
    db: Session = Depends(get_db)
):
    """
    Get total count of online users
    """
    return await OnlineStatusService.get_total_online_users(db, timeout_minutes)


@router.post("/cleanup-expired", status_code=status.HTTP_200_OK)
async def cleanup_expired_sessions(
    timeout_minutes: int = Query(60, description="Timeout in minutes for considering session expired"),
    db: Session = Depends(get_db)
):
    """
    Clean up expired sessions
    """
    cleaned_count = await OnlineStatusService.cleanup_expired_sessions(db, timeout_minutes)
    return {"cleaned_sessions": cleaned_count}
