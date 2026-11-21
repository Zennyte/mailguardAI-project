from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core import security
from app.core.cookies import ACCESS_TOKEN_COOKIE
from app.core.database import get_db
from app.models import User
from app.repositories import user_repository


# Gjen perdoruesin e kycur nga cookie-ja "access_token" qe shfletuesi e dergon vetem.
# Perdoret ne controller si: current_user: User = Depends(get_current_user)
def get_current_user(
    access_token: str | None = Cookie(default=None, alias=ACCESS_TOKEN_COOKIE),
    db: Session = Depends(get_db),
) -> User:
    if access_token is None:
        raise HTTPException(status_code=401, detail="Not logged in")

    user_id = security.read_user_id_from_access_token(access_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = user_repository.find_user_by_id(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


# Lejon vetem perdoruesit qe kane nje leje te caktuar (lejet vijne nga rolet).
# Perdoret ne controller si: Depends(require_permission("manage_cms"))
def require_permission(permission_name: str):
    def check_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        user_permissions = user_repository.get_permission_names(db, current_user.id)
        if permission_name not in user_permissions:
            raise HTTPException(status_code=403, detail=f"Requires permission: {permission_name}")
        return current_user

    return check_permission
