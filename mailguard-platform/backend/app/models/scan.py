from sqlalchemy import (
    Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey, Numeric, UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class ModelVersion(Base):
    __tablename__ = "model_versions"
    __table_args__ = (UniqueConstraint("model_name", "version"),)

    id = Column(BigInteger, primary_key=True)
    model_name = Column(String(100), nullable=False)
    version = Column(String(20), nullable=False)
    file_path = Column(String(500))
    is_active = Column(Boolean, nullable=False, default=False)
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class ScanRequest(Base):
    __tablename__ = "scan_requests"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    email_message_id = Column(BigInteger, ForeignKey("email_messages.id", ondelete="SET NULL"))
    status = Column(String(20), nullable=False, default="pending", index=True)  # pending / completed / failed
    input_type = Column(String(20), nullable=False, default="paste")  # paste / upload
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Nje kerkese skanimi ka nje rezultat te vetem
    result = relationship("ScanResult", uselist=False, cascade="all, delete-orphan")


class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(BigInteger, primary_key=True)
    scan_request_id = Column(BigInteger, ForeignKey("scan_requests.id", ondelete="CASCADE"), nullable=False, unique=True)
    predicted_label = Column(String(20), nullable=False, index=True)  # safe / spam / phishing
    confidence_score = Column(Numeric(5, 4))
    model_version_id = Column(BigInteger, ForeignKey("model_versions.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Probabiliteti per cdo klase (safe/spam/phishing)
    scores = relationship("ClassificationScore", cascade="all, delete-orphan")


class ClassificationScore(Base):
    __tablename__ = "classification_scores"

    id = Column(BigInteger, primary_key=True)
    scan_result_id = Column(BigInteger, ForeignKey("scan_results.id", ondelete="CASCADE"), nullable=False, index=True)
    label = Column(String(20), nullable=False)
    score = Column(Numeric(5, 4), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class UserFeedback(Base):
    __tablename__ = "user_feedback"

    id = Column(BigInteger, primary_key=True)
    scan_result_id = Column(BigInteger, ForeignKey("scan_results.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    correct_label = Column(String(20))
    comment = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
