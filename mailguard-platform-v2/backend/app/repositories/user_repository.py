from sqlalchemy.orm import Session

from app.models import User, Role, UserRole, Permission, RolePermission


def find_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def find_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, first_name: str, last_name: str, email: str, password_hash: str) -> User:
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password_hash=password_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# I jep perdoruesit nje rol (p.sh. "User"). Kthen False nese roli nuk ekziston
# ne databaze - ne ate rast seed.sql nuk eshte ekzekutuar ende.
def assign_role_to_user(db: Session, user_id: int, role_name: str) -> bool:
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None:
        return False
    db.add(UserRole(user_id=user_id, role_id=role.id))
    db.commit()
    return True


# Emrat e roleve te perdoruesit, p.sh. ["User"] ose ["Admin"]
def get_role_names(db: Session, user_id: int) -> list:
    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return [row[0] for row in rows]


# Emrat e lejeve te perdoruesit - lejet vijne nga rolet qe ai ka
def get_permission_names(db: Session, user_id: int) -> list:
    rows = (
        db.query(Permission.name)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .filter(UserRole.user_id == user_id)
        .distinct()
        .all()
    )
    return [row[0] for row in rows]
