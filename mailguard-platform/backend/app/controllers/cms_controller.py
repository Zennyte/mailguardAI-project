from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_permission
from app.models import User
from app.schemas.cms import (
    CmsPageCreateRequest, CmsPageUpdateRequest, CmsPageResponse,
    CmsBlockCreateRequest, CmsBlockResponse,
)
from app.services import cms_service

router = APIRouter(prefix="/cms", tags=["CMS"])


# Endpoints publike (permbajtja e publikuar)

# GET /cms/pages - lista publike e faqeve te publikuara
@router.get("/pages", response_model=list[CmsPageResponse])
def get_published_pages(db: Session = Depends(get_db)):
    return cms_service.list_published_pages(db)


# Kujdes: "/pages/manage" duhet te deklarohet para "/pages/{slug}"
@router.get("/pages/manage", response_model=list[CmsPageResponse])
def get_all_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.list_all_pages(db)


# GET /cms/pages/{slug} - nje faqe e publikuar, sipas slug
@router.get("/pages/{slug}", response_model=CmsPageResponse)
def get_page_by_slug(slug: str, db: Session = Depends(get_db)):
    return cms_service.get_published_page(db, slug)


# Endpoints te mbrojtura (menaxhimi i permbajtjes)

# POST /cms/pages - krijon nje faqe te re (kerkon manage_cms)
@router.post("/pages", response_model=CmsPageResponse, status_code=201)
def create_page(
    data: CmsPageCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.create_page(db, current_user.id, data)


# PUT /cms/pages/{id} - perditeson nje faqe (kerkon manage_cms)
@router.put("/pages/{page_id}", response_model=CmsPageResponse)
def update_page(
    page_id: int,
    data: CmsPageUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.update_page(db, current_user.id, page_id, data)


# DELETE /cms/pages/{id} - fshin nje faqe (kerkon manage_cms)
@router.delete("/pages/{page_id}")
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.delete_page(db, page_id)


# POST /cms/pages/{id}/blocks - shton nje bllok permbajtjeje
@router.post("/pages/{page_id}/blocks", response_model=CmsBlockResponse, status_code=201)
def add_block(
    page_id: int,
    data: CmsBlockCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.add_block(db, page_id, data)


# PUT /cms/blocks/{id} - perditeson nje bllok
@router.put("/blocks/{block_id}", response_model=CmsBlockResponse)
def update_block(
    block_id: int,
    data: CmsBlockCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.update_block(db, block_id, data)


# DELETE /cms/blocks/{id} - fshin nje bllok
@router.delete("/blocks/{block_id}")
def delete_block(
    block_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.delete_block(db, block_id)
