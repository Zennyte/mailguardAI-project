from sqlalchemy.orm import Session

from app.models import CmsPage, CmsContentBlock


# Lista e faqeve CMS (te publikuara ose te gjitha)
def list_pages(db: Session, published_only: bool):
    query = db.query(CmsPage)
    if published_only:
        query = query.filter(CmsPage.is_published == True)  # noqa: E712
    return query.order_by(CmsPage.id).all()


# Gjen nje faqe CMS sipas slug
def get_page_by_slug(db: Session, slug: str):
    return db.query(CmsPage).filter(CmsPage.slug == slug).first()


# Gjen nje faqe CMS sipas id
def get_page_by_id(db: Session, page_id: int):
    return db.query(CmsPage).filter(CmsPage.id == page_id).first()


# Fut nje faqe te re CMS ne DB
def create_page(db: Session, user_id: int, title: str, slug: str, is_published: bool) -> CmsPage:
    page = CmsPage(title=title, slug=slug, is_published=is_published, created_by=user_id)
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


# Perditeson fushat e nje faqeje CMS
def update_page(db: Session, page: CmsPage, user_id: int,
                title: str, slug: str, is_published: bool) -> CmsPage:
    page.title = title
    page.slug = slug
    page.is_published = is_published
    page.updated_by = user_id
    db.commit()
    db.refresh(page)
    return page


# Fshin nje faqe CMS
def delete_page(db: Session, page: CmsPage):
    # Blloqet fshihen bashke me faqen (cascade)
    db.delete(page)
    db.commit()


# Fut nje bllok te ri permbajtjeje
def add_block(db: Session, page_id: int, block_type: str,
              content, sort_order: int) -> CmsContentBlock:
    block = CmsContentBlock(cms_page_id=page_id, block_type=block_type,
                            content=content, sort_order=sort_order)
    db.add(block)
    db.commit()
    db.refresh(block)
    return block


# Gjen nje bllok sipas id
def get_block_by_id(db: Session, block_id: int):
    return db.query(CmsContentBlock).filter(CmsContentBlock.id == block_id).first()


# Perditeson fushat e nje blloku
def update_block(db: Session, block: CmsContentBlock, block_type: str,
                 content, sort_order: int) -> CmsContentBlock:
    block.block_type = block_type
    block.content = content
    block.sort_order = sort_order
    db.commit()
    db.refresh(block)
    return block


# Fshin nje bllok permbajtjeje
def delete_block(db: Session, block: CmsContentBlock):
    db.delete(block)
    db.commit()
