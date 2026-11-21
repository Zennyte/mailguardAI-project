from sqlalchemy import Column, BigInteger, String, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela import_jobs - nje rresht per cdo import te bere ne faqen Import/Export
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


# Tabela export_jobs - nje rresht per cdo eksport te bere ne faqen Import/Export
class ExportJob(Base):
    __tablename__ = "export_jobs"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    export_type = Column(String(20), nullable=False, default="csv")  # csv / json / xlsx
    file_id = Column(BigInteger, ForeignKey("files.id", ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
