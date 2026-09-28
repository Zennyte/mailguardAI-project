from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core import security
from app.core.database import get_db
from app.models import User
from app.repositories import user_repository

bearer_scheme = HTTPBearer()


# Lexon JWT-ne nga header-i Authorization dhe kthen perdoruesin
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    # Lexojme tokenin nga headeri "Authorization: Bearer ..."
    user_id = security.decode_access_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = user_repository.get_by_id(db, user_id)
    if user is None or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user


# Dependency qe kerkon nje rol specifik (p.sh. Admin)
def require_role(role_name: str):
    # Perdoret si: Depends(require_role("Admin"))
    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        roles = user_repository.get_role_names(db, current_user.id)
        if role_name not in roles:
            raise HTTPException(status_code=403, detail=f"Requires role: {role_name}")
        return current_user

    return checker


# Dependency qe kerkon nje leje specifike (p.sh. manage_cms)
def require_permission(permission_name: str):
    # Perdoret si: Depends(require_permission("scan_email"))
    def checker(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ) -> User:
        permissions = user_repository.get_permission_names(db, current_user.id)
        if permission_name not in permissions:
            raise HTTPException(status_code=403, detail=f"Requires permission: {permission_name}")
        return current_user

    return checker
