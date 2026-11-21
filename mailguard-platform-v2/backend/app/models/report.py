from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela reports - raportet e gjeneruara nga perdoruesi
class Report(Base):
    __tablename__ = "reports"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    report_name = Column(String(200), nullable=False)
    report_type = Column(String(50))  # p.sh. scan_summary / label_distribution
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    filters = relationship("ReportFilter", cascade="all, delete-orphan")


# Tabela report_filters - filtrat e perdorur per nje raport
class ReportFilter(Base):
    __tablename__ = "report_filters"

    id = Column(BigInteger, primary_key=True)
    report_id = Column(BigInteger, ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, index=True)
    filter_key = Column(String(100), nullable=False)
    filter_value = Column(String(255))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
