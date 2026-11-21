# Faqet: Login (/login), Register (/register) dhe butoni Logout.
# Tokenat e kycjes dergohen dhe lexohen vetem si cookie "httpOnly" (shiko core/cookies.py).
from fastapi import APIRouter, Cookie, Depends, Response
from sqlalchemy.orm import Session

from app.core import cookies
from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models import User
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


# POST /auth/register - krijon nje llogari te re
@router.post("/register", response_model=UserResponse, status_code=201)
def register(form: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(db, form)


# POST /auth/login - kthen perdoruesin dhe vendos tokenat ne cookie
@router.post("/login", response_model=UserResponse)
def login(form: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user, access_token, refresh_token = auth_service.login_user(db, form)
    cookies.set_login_cookies(response, access_token, refresh_token)
    return user


# POST /auth/refresh - nderron refresh tokenin (nga cookie) me nje cift te ri tokenash
@router.post("/refresh")
def refresh_tokens(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=cookies.REFRESH_TOKEN_COOKIE),
    db: Session = Depends(get_db),
):
    new_access_token, new_refresh_token = auth_service.refresh_tokens(db, refresh_token)
    cookies.set_login_cookies(response, new_access_token, new_refresh_token)
    return {"message": "Tokens refreshed"}


# POST /auth/logout - revokon refresh tokenin dhe fshin cookie-t
@router.post("/logout")
def logout(
    response: Response,
    refresh_token: str | None = Cookie(default=None, alias=cookies.REFRESH_TOKEN_COOKIE),
    db: Session = Depends(get_db),
):
    auth_service.logout_user(db, refresh_token)
    cookies.clear_login_cookies(response)
    return {"message": "Logged out successfully"}


# GET /auth/me - perdoruesi i kycur, me rolet dhe lejet e tij
@router.get("/me", response_model=UserResponse)
def get_logged_in_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return auth_service.build_user_response(db, current_user)
