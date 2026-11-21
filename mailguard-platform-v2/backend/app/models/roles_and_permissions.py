from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func

from app.core.database import Base

# Si funksionon: perdoruesi ka role (user_roles), roli ka leje (role_permissions).
# P.sh. roli "Admin" ka lejen "manage_cms".


# Tabela roles - rolet e perdoruesve (Admin, Manager, User)
class Role(Base):
    __tablename__ = "roles"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


# Tabela user_roles - cili perdorues ka cilin rol (many-to-many)
class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = (UniqueConstraint("user_id", "role_id"),)

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


# Tabela permissions - lejet individuale (scan_email, manage_cms, import_data, ...)
class Permission(Base):
    __tablename__ = "permissions"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


# Tabela role_permissions - cili rol ka cilen leje (many-to-many)
class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = (UniqueConstraint("role_id", "permission_id"),)

    id = Column(BigInteger, primary_key=True)
    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False, index=True)
    permission_id = Column(BigInteger, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
