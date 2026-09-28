from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.models import AuditLog, User
from app.repositories import user_repository, token_repository
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

DEFAULT_ROLE = "User"


# Regjistron nje perdorues te ri dhe i cakton rolin default
def register_user(db: Session, data: RegisterRequest) -> UserResponse:
    # Kontrollojme nese perdoruesi ekziston
    if user_repository.get_by_email(db, data.email) is not None:
        raise HTTPException(status_code=400, detail="Email is already registered")

    password_hash = security.hash_password(data.password)
    user = user_repository.create(db, data.first_name, data.last_name, data.email, password_hash)

    # Perdoruesit e rinj marrin rolin "User" (nga seed.sql)
    user_repository.assign_role(db, user.id, DEFAULT_ROLE)
    log_action(db, user.id, "register")
    return build_user_response(db, user)


# Verifikon kredencialet dhe kthen access + refresh token
def login_user(db: Session, data: LoginRequest) -> TokenResponse:
    user = user_repository.get_by_email(db, data.email)
    if user is None or not security.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="This account is deactivated")

    tokens = create_tokens(db, user.id)
    log_action(db, user.id, "login")
    return tokens


# Verifikon refresh tokenin dhe kthen nje cift te ri (rotation)
def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
    token_hash = security.hash_refresh_token(refresh_token)
    saved_token = token_repository.get_valid(db, token_hash)
    if saved_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Tokeni i vjeter revokohet dhe krijohet nje cift i ri
    token_repository.revoke(db, token_hash)
    return create_tokens(db, saved_token.user_id)


# Revokon refresh tokenin e perdoruesit
def logout_user(db: Session, refresh_token: str, user_id: int) -> dict:
    token_hash = security.hash_refresh_token(refresh_token)
    token_repository.revoke(db, token_hash)
    log_action(db, user_id, "logout")
    return {"message": "Logged out successfully"}


# Krijon dhe ruan (te hash-uar) nje cift access+refresh token
def create_tokens(db: Session, user_id: int) -> TokenResponse:
    access_token = security.create_access_token(user_id)
    refresh_token = security.create_refresh_token()
    token_repository.save(db, user_id, security.hash_refresh_token(refresh_token))
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


# Ndertimi i UserResponse me rolet e perdoruesit
def build_user_response(db: Session, user: User) -> UserResponse:
    return UserResponse(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        roles=user_repository.get_role_names(db, user.id),
    )


# Regjistron nje veprim ne audit_logs
def log_action(db: Session, user_id: int, action: str):
    # Regjistrojme veprimin ne audit_logs
    db.add(AuditLog(user_id=user_id, action=action, entity="user", entity_id=user_id))
    db.commit()
