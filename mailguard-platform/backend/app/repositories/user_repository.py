from sqlalchemy.orm import Session

from app.models import User, Role, UserRole, Permission, RolePermission


# Gjen nje perdorues sipas email-it
def get_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# Gjen nje perdorues sipas id-se
def get_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# Krijon nje llogari te re perdoruesi
def create(db: Session, first_name: str, last_name: str, email: str, password_hash: str) -> User:
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


# I cakton perdoruesit nje rol (p.sh. User, Admin)
def assign_role(db: Session, user_id: int, role_name: str) -> bool:
    # Kthen False nese roli nuk ekziston (seed.sql duhet ekzekutuar me pare)
    role = db.query(Role).filter(Role.name == role_name).first()
    if role is None:
        return False
    db.add(UserRole(user_id=user_id, role_id=role.id))
    db.commit()
    return True


# Kthen emrat e roleve qe ka nje perdorues
def get_role_names(db: Session, user_id: int) -> list:
    rows = (
        db.query(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )
    return [row[0] for row in rows]


# Kthen lejet e perdoruesit (te derivuara nga rolet e tij)
def get_permission_names(db: Session, user_id: int) -> list:
    # Lejet e perdoruesit vijne nga rolet qe ai ka
    rows = (
        db.query(Permission.name)
        .join(RolePermission, RolePermission.permission_id == Permission.id)
        .join(UserRole, UserRole.role_id == RolePermission.role_id)
        .filter(UserRole.user_id == user_id)
        .distinct()
        .all()
    )
    return [row[0] for row in rows]
