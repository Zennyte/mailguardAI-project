from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.auth import (
    RegisterRequest, LoginRequest, RefreshTokenRequest, TokenResponse, UserResponse,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


# POST /auth/register - krijon nje llogari te re
@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


# POST /auth/login - kthen access + refresh token
@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(db, data)


# POST /auth/refresh - rrotullon refresh tokenin dhe jep nje cift te ri
@router.post("/refresh", response_model=TokenResponse)
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):
    return auth_service.refresh_access_token(db, data.refresh_token)


# POST /auth/logout - revokon refresh tokenin
@router.post("/logout")
def logout(
    data: RefreshTokenRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return auth_service.logout_user(db, data.refresh_token, current_user.id)


# GET /auth/me - kthen te dhenat e perdoruesit te kycur
@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return auth_service.build_user_response(db, current_user)
