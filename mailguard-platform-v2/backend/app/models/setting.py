from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela settings - konfigurime globale ne formen key/value
class Setting(Base):
    __tablename__ = "settings"

    id = Column(BigInteger, primary_key=True)
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(String(255))
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
