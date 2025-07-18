from fastapi import APIRouter, Depends, status, Header, Request
from sqlalchemy.orm import Session
from app.services.auth import AuthService
from app.services.otp_auth import OTPAuthService
from app.db.database import get_db
from app.models.user_session import UserSession
from sqlalchemy import func
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
<<<<<<< HEAD
from app.schemas.auth import Signup, UserOut
from app.schemas.otp import UserBaseSchema, LoginUserSchema, UserRequestSchema

=======
from app.schemas.auth import UserOut, Signup
from app.schemas.otp import UserBaseSchema, LoginUserSchema, UserRequestSchema
from app.services.auth import AuthService
>>>>>>> b600bb7 (fifth commit)

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/token")
async def user_login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    #return await AuthService.login(request, user_credentials, db)
    return await AuthService.login(user_credentials=user_credentials, db=db, request=request)

@router.post("/signup", status_code=status.HTTP_200_OK, response_model=UserOut)
async def user_signup(
        user: Signup,
        db: Session = Depends(get_db)):
    return await AuthService.signup(db, user)

@router.post("/login", status_code=status.HTTP_200_OK)
async def user_login(
        request: Request,
        user_credentials: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    return await AuthService.login(user_credentials=user_credentials, db=db, request=request)
@router.post("/register-otp", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserBaseSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.register_user(db, user)


<<<<<<< HEAD
@router.post("/register-otp", status_code=status.HTTP_201_CREATED)
async def register_user(
        user: UserBaseSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.register_user(db, user)


=======
>>>>>>> b600bb7 (fifth commit)
@router.post("/login-otp", status_code=status.HTTP_200_OK)
async def login_user(
        payload: LoginUserSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.login_user(db, payload)


@router.post("/otp/generate", status_code=status.HTTP_200_OK)
async def generate_otp(
        payload: UserRequestSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.generate_otp(db, payload.user_id)


@router.post("/otp/verify", status_code=status.HTTP_200_OK)
async def verify_otp(
        payload: UserRequestSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.verify_otp(db, payload.user_id, payload.token)


@router.post("/otp/validate", status_code=status.HTTP_200_OK)
async def validate_otp(
        payload: UserRequestSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.validate_otp(db, payload.user_id, payload.token)


@router.post("/otp/disable", status_code=status.HTTP_200_OK)
async def disable_otp(
        payload: UserRequestSchema,
        db: Session = Depends(get_db)):
    return await OTPAuthService.disable_otp(db, payload.user_id)

<<<<<<< HEAD

=======
>>>>>>> b600bb7 (fifth commit)
@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(
        refresh_token: str = Header(),
        db: Session = Depends(get_db)):
    return await AuthService.get_refresh_token(token=refresh_token, db=db)

@router.get("/online-users")
def get_online_users(db: Session = Depends(get_db)):
    active_sessions = db.query(
        User.role,
        func.count(User.id).label("count")
    ).join(UserSession, User.id == UserSession.user_id)\
     .filter(UserSession.is_active == True)\
     .group_by(User.role).all()

    return {"online_users_by_role": [{"role": r, "count": c} for r, c in active_sessions]}
