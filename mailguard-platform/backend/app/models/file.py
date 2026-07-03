from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(BigInteger, primary_key=True)
    original_name = Column(String(255), nullable=False)
    stored_name = Column(String(255), nullable=False)
    mime_type = Column(String(100))
    file_size = Column(BigInteger)
    file_path = Column(String(500))
    uploaded_by = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
