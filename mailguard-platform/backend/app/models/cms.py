from sqlalchemy import Column, BigInteger, String, Text, Boolean, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


# Tabela cms_pages - faqet e thjeshta CMS
class CmsPage(Base):
    __tablename__ = "cms_pages"

    id = Column(BigInteger, primary_key=True)
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    is_published = Column(Boolean, nullable=False, default=False)
    created_by = Column(BigInteger, ForeignKey("users.id"))
    updated_by = Column(BigInteger, ForeignKey("users.id"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    # Blloqet e permbajtjes te renditura sipas sort_order
    blocks = relationship("CmsContentBlock", cascade="all, delete-orphan",
                          order_by="CmsContentBlock.sort_order")


# Tabela cms_content_blocks - blloqet e permbajtjes se nje faqeje
class CmsContentBlock(Base):
    __tablename__ = "cms_content_blocks"

    id = Column(BigInteger, primary_key=True)
    cms_page_id = Column(BigInteger, ForeignKey("cms_pages.id", ondelete="CASCADE"), nullable=False, index=True)
    block_type = Column(String(50), nullable=False, default="text")  # text / image / list
    content = Column(Text)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
