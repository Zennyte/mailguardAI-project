from sqlalchemy import Column, BigInteger, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela settings - konfigurime globale key/value
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


# Tabela import_jobs - importimi masiv i emaileve
class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default="pending")  # pending / processing / completed / failed
    total_rows = Column(Integer, nullable=False, default=0)
    processed_rows = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


# Tabela export_jobs - eksportimi i te dhenave
class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    export_type = Column(String(20), nullable=False, default="csv")  # csv / json
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
