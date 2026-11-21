from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.models import User
from app.repositories import user_repository, refresh_token_repository, audit_log_repository
from app.schemas.auth import RegisterRequest, LoginRequest, UserResponse

# Roli qe merr cdo llogari e re (rolet krijohen nga database/seed.sql)
DEFAULT_ROLE_NAME = "User"


def register_user(db: Session, form: RegisterRequest) -> UserResponse:
    if user_repository.find_user_by_email(db, form.email) is not None:
        raise HTTPException(status_code=400, detail="Email is already registered")

    password_hash = security.hash_password(form.password)
    user = user_repository.create_user(db, form.first_name, form.last_name, form.email, password_hash)

    user_repository.assign_role_to_user(db, user.id, DEFAULT_ROLE_NAME)
    audit_log_repository.add_user_action(db, user.id, "register")
    return build_user_response(db, user)


# Kontrollon email-in dhe fjalekalimin. Kthen (perdoruesin, access_token, refresh_token);
# controller i vendos tokenat ne cookie, ata nuk i shihen kurre JavaScript-it.
def login_user(db: Session, form: LoginRequest):
    user = user_repository.find_user_by_email(db, form.email)
    if user is None or not security.verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="This account is deactivated")

    access_token, refresh_token = create_token_pair(db, user.id)
    audit_log_repository.add_user_action(db, user.id, "login")
    return build_user_response(db, user), access_token, refresh_token


# Kur access tokeni skadon (pas 30 min), shfletuesi dergon refresh tokenin dhe merr nje cift te ri.
# Refresh tokeni i vjeter revokohet, keshtu secili perdoret vetem njehere.
def refresh_tokens(db: Session, refresh_token: str | None):
    if refresh_token is None:
        raise HTTPException(status_code=401, detail="Not logged in")

    token_hash = security.hash_refresh_token(refresh_token)
    saved_refresh_token = refresh_token_repository.find_valid_refresh_token(db, token_hash)
    if saved_refresh_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    refresh_token_repository.revoke_refresh_token(db, token_hash)
    return create_token_pair(db, saved_refresh_token.user_id)


# Revokon refresh tokenin ne databaze (controller fshin edhe cookie-t).
# Funksionon edhe nese access tokeni ka skaduar - logout duhet te mundet gjithmone.
def logout_user(db: Session, refresh_token: str | None):
    if refresh_token is None:
        return
    token_hash = security.hash_refresh_token(refresh_token)
    user_id = refresh_token_repository.revoke_refresh_token(db, token_hash)
    if user_id is not None:
        audit_log_repository.add_user_action(db, user_id, "logout")


# Krijon access token + refresh token; ne databaze ruan vetem hash-in e refresh tokenit
def create_token_pair(db: Session, user_id: int):
    access_token = security.create_access_token(user_id)
    refresh_token = security.create_refresh_token()
    refresh_token_repository.save_refresh_token(db, user_id, security.hash_refresh_token(refresh_token))
    return access_token, refresh_token


# Frontend-i i perdor rolet dhe lejet per te fshehur/shfaqur pjese te faqes
def build_user_response(db: Session, user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        roles=user_repository.get_role_names(db, user.id),
        permissions=user_repository.get_permission_names(db, user.id),
    )
