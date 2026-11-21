from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela notifications - njoftimet e perdoruesit
class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(Text)
    notification_type = Column(String(50))
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
