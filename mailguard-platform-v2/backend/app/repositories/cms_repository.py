from sqlalchemy.orm import Session

from app.models import CmsPage, CmsContentBlock


# ---------- Faqet CMS ----------

def get_all_pages(db: Session):
    return db.query(CmsPage).order_by(CmsPage.id).all()


def find_page_by_slug(db: Session, slug: str):
    return db.query(CmsPage).filter(CmsPage.slug == slug).first()


def find_page_by_id(db: Session, page_id: int):
    return db.query(CmsPage).filter(CmsPage.id == page_id).first()


def create_page(db: Session, user_id: int, title: str, slug: str, is_published: bool) -> CmsPage:
    page = CmsPage(title=title, slug=slug, is_published=is_published, created_by=user_id)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


def update_page(db: Session, page: CmsPage, user_id: int,
                title: str, slug: str, is_published: bool) -> CmsPage:
    page.title = title
    page.slug = slug
    page.is_published = is_published
    page.updated_by = user_id
    db.commit()
    db.refresh(page)
    return page


# Blloqet e faqes fshihen bashke me faqen (cascade)
def delete_page(db: Session, page: CmsPage):
    db.delete(page)
    db.commit()


# ---------- Blloqet e permbajtjes ----------

def find_block_by_id(db: Session, block_id: int):
    return db.query(CmsContentBlock).filter(CmsContentBlock.id == block_id).first()


def create_block(db: Session, page_id: int, block_type: str,
                 content, sort_order: int) -> CmsContentBlock:
    block = CmsContentBlock(cms_page_id=page_id, block_type=block_type,
                            content=content, sort_order=sort_order)
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


def update_block(db: Session, block: CmsContentBlock, block_type: str,
                 content, sort_order: int) -> CmsContentBlock:
    block.block_type = block_type
    block.content = content
    block.sort_order = sort_order
    db.commit()
    db.refresh(block)
    return block


def delete_block(db: Session, block: CmsContentBlock):
    db.delete(block)
    db.commit()
