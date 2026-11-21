from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import cms_repository
from app.schemas.cms import (
    CmsPageSaveRequest, CmsPageResponse, CmsBlockSaveRequest, CmsBlockResponse,
)


# ---------- Pjesa publike (kushdo mund ta lexoje permbajtjen e publikuar) ----------

# Perdoret nga Homepage per te lexuar faqen me slug "home"
def get_published_page(db: Session, slug: str) -> CmsPageResponse:
    page = cms_repository.find_page_by_slug(db, slug)
    if page is None or not page.is_published:
        raise HTTPException(status_code=404, detail="Page not found")
    return CmsPageResponse.model_validate(page)


# ---------- Paneli i menaxhimit (faqja CMS, vetem me lejen manage_cms) ----------

# Te gjitha faqet, perfshire draftet
def get_all_pages(db: Session) -> list:
    pages = cms_repository.get_all_pages(db)
    return [CmsPageResponse.model_validate(page) for page in pages]


def create_page(db: Session, user_id: int, form: CmsPageSaveRequest) -> CmsPageResponse:
    # Slug-u duhet te jete unik
    if cms_repository.find_page_by_slug(db, form.slug) is not None:
        raise HTTPException(status_code=400, detail="A page with this slug already exists")
    page = cms_repository.create_page(db, user_id, form.title, form.slug, form.is_published)
    return CmsPageResponse.model_validate(page)


def update_page(db: Session, user_id: int, page_id: int, form: CmsPageSaveRequest) -> CmsPageResponse:
    page = cms_repository.find_page_by_id(db, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    # Slug-u i ri nuk duhet t'i perkase nje faqeje tjeter
    page_with_same_slug = cms_repository.find_page_by_slug(db, form.slug)
    if page_with_same_slug is not None and page_with_same_slug.id != page_id:
        raise HTTPException(status_code=400, detail="A page with this slug already exists")

    page = cms_repository.update_page(db, page, user_id, form.title, form.slug, form.is_published)
    return CmsPageResponse.model_validate(page)


def delete_page(db: Session, page_id: int) -> dict:
    page = cms_repository.find_page_by_id(db, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    cms_repository.delete_page(db, page)
    return {"message": "Page deleted"}


def add_block_to_page(db: Session, page_id: int, form: CmsBlockSaveRequest) -> CmsBlockResponse:
    if cms_repository.find_page_by_id(db, page_id) is None:
        raise HTTPException(status_code=404, detail="Page not found")
    block = cms_repository.create_block(db, page_id, form.block_type, form.content, form.sort_order)
    return CmsBlockResponse.model_validate(block)


def update_block(db: Session, block_id: int, form: CmsBlockSaveRequest) -> CmsBlockResponse:
    block = cms_repository.find_block_by_id(db, block_id)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    block = cms_repository.update_block(db, block, form.block_type, form.content, form.sort_order)
    return CmsBlockResponse.model_validate(block)


def delete_block(db: Session, block_id: int) -> dict:
    block = cms_repository.find_block_by_id(db, block_id)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    cms_repository.delete_block(db, block)
    return {"message": "Block deleted"}
