from sqlalchemy import Column, BigInteger, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class EmailMessage(Base):
    __tablename__ = "email_messages"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    subject = Column(String(500))
    body_preview = Column(Text)
    source_type = Column(String(20), nullable=False, default="pasted")  # pasted / uploaded / imported
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Pjeset e emailit fshihen bashke me emailin
    headers = relationship("EmailHeader", cascade="all, delete-orphan")
    recipients = relationship("EmailRecipient", cascade="all, delete-orphan")
    links = relationship("EmailLink", cascade="all, delete-orphan")
    attachments = relationship("EmailAttachment", cascade="all, delete-orphan")


class EmailHeader(Base):
    __tablename__ = "email_headers"

    id = Column(BigInteger, primary_key=True)
    email_message_id = Column(BigInteger, ForeignKey("email_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    header_name = Column(String(100), nullable=False)
    header_value = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class EmailRecipient(Base):
    __tablename__ = "email_recipients"

    id = Column(BigInteger, primary_key=True)
    email_message_id = Column(BigInteger, ForeignKey("email_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    recipient_email = Column(String(255), nullable=False)
    recipient_type = Column(String(10), nullable=False, default="to")  # to / cc / bcc
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class EmailLink(Base):
    __tablename__ = "email_links"

    id = Column(BigInteger, primary_key=True)
    email_message_id = Column(BigInteger, ForeignKey("email_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    url = Column(Text, nullable=False)
    domain = Column(String(255))
    is_suspicious = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())


class EmailAttachment(Base):
    __tablename__ = "email_attachments"

    id = Column(BigInteger, primary_key=True)
    email_message_id = Column(BigInteger, ForeignKey("email_messages.id", ondelete="CASCADE"), nullable=False, index=True)
    filename = Column(String(255))
    mime_type = Column(String(100))
    file_size = Column(BigInteger)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
