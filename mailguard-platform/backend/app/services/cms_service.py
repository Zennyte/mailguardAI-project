from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import cms_repository
from app.schemas.cms import (
    CmsPageCreateRequest, CmsPageUpdateRequest, CmsPageResponse,
    CmsBlockCreateRequest, CmsBlockResponse,
)


def list_published_pages(db: Session) -> list:
    pages = cms_repository.list_pages(db, published_only=True)
    return [CmsPageResponse.model_validate(p) for p in pages]


def list_all_pages(db: Session) -> list:
    # Per panelin e menaxhimit - perfshin edhe draftet
    pages = cms_repository.list_pages(db, published_only=False)
    return [CmsPageResponse.model_validate(p) for p in pages]


def get_published_page(db: Session, slug: str) -> CmsPageResponse:
    page = cms_repository.get_page_by_slug(db, slug)
    if page is None or not page.is_published:
        raise HTTPException(status_code=404, detail="Page not found")
    return CmsPageResponse.model_validate(page)


def create_page(db: Session, user_id: int, data: CmsPageCreateRequest) -> CmsPageResponse:
    # Kontrollojme nese slug-u ekziston
    if cms_repository.get_page_by_slug(db, data.slug):
        raise HTTPException(status_code=400, detail="A page with this slug already exists")
    page = cms_repository.create_page(db, user_id, data.title, data.slug, data.is_published)
    return CmsPageResponse.model_validate(page)


def update_page(db: Session, user_id: int, page_id: int,
                data: CmsPageUpdateRequest) -> CmsPageResponse:
    page = cms_repository.get_page_by_id(db, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")

    existing = cms_repository.get_page_by_slug(db, data.slug)
    if existing is not None and existing.id != page_id:
        raise HTTPException(status_code=400, detail="A page with this slug already exists")

    page = cms_repository.update_page(db, page, user_id, data.title, data.slug, data.is_published)
    return CmsPageResponse.model_validate(page)


def delete_page(db: Session, page_id: int) -> dict:
    page = cms_repository.get_page_by_id(db, page_id)
    if page is None:
        raise HTTPException(status_code=404, detail="Page not found")
    cms_repository.delete_page(db, page)
    return {"message": "Page deleted"}


def add_block(db: Session, page_id: int, data: CmsBlockCreateRequest) -> CmsBlockResponse:
    if cms_repository.get_page_by_id(db, page_id) is None:
        raise HTTPException(status_code=404, detail="Page not found")
    block = cms_repository.add_block(db, page_id, data.block_type, data.content, data.sort_order)
    return CmsBlockResponse.model_validate(block)


def update_block(db: Session, block_id: int, data: CmsBlockCreateRequest) -> CmsBlockResponse:
    block = cms_repository.get_block_by_id(db, block_id)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    block = cms_repository.update_block(db, block, data.block_type, data.content, data.sort_order)
    return CmsBlockResponse.model_validate(block)


def delete_block(db: Session, block_id: int) -> dict:
    block = cms_repository.get_block_by_id(db, block_id)
    if block is None:
        raise HTTPException(status_code=404, detail="Block not found")
    cms_repository.delete_block(db, block)
    return {"message": "Block deleted"}
