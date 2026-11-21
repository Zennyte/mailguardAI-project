# Faqet: CMS (/cms) per menaxhim dhe Homepage (/) per leximin e faqes "home"
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import require_permission
from app.core.database import get_db
from app.models import User
from app.schemas.cms import (
    CmsPageSaveRequest, CmsPageResponse, CmsBlockSaveRequest, CmsBlockResponse,
)
from app.services import cms_service

router = APIRouter(prefix="/cms", tags=["CMS"])


# ---------- Publike (pa kycje) ----------

# GET /cms/pages/{slug} - nje faqe e publikuar (Homepage kerkon slug-un "home")
@router.get("/pages/{slug}", response_model=CmsPageResponse)
def get_published_page(slug: str, db: Session = Depends(get_db)):
    return cms_service.get_published_page(db, slug)


# ---------- Menaxhimi (kerkon lejen manage_cms) ----------

# GET /cms/manage/pages - te gjitha faqet, edhe draftet (lista ne faqen CMS)
@router.get("/manage/pages", response_model=list[CmsPageResponse])
def get_all_pages(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.get_all_pages(db)


# POST /cms/pages - forma "New page"
@router.post("/pages", response_model=CmsPageResponse, status_code=201)
def create_page(
    form: CmsPageSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.create_page(db, current_user.id, form)


# PUT /cms/pages/{id} - butoni "Save Page"
@router.put("/pages/{page_id}", response_model=CmsPageResponse)
def update_page(
    page_id: int,
    form: CmsPageSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.update_page(db, current_user.id, page_id, form)


# DELETE /cms/pages/{id} - butoni "Delete" prane nje faqeje
@router.delete("/pages/{page_id}")
def delete_page(
    page_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.delete_page(db, page_id)


# POST /cms/pages/{id}/blocks - butoni "Add Block"
@router.post("/pages/{page_id}/blocks", response_model=CmsBlockResponse, status_code=201)
def add_block_to_page(
    page_id: int,
    form: CmsBlockSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.add_block_to_page(db, page_id, form)


# PUT /cms/blocks/{id} - butoni "Save" i nje blloku
@router.put("/blocks/{block_id}", response_model=CmsBlockResponse)
def update_block(
    block_id: int,
    form: CmsBlockSaveRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.update_block(db, block_id, form)


# DELETE /cms/blocks/{id} - butoni "Delete" i nje blloku
@router.delete("/blocks/{block_id}")
def delete_block(
    block_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("manage_cms")),
):
    return cms_service.delete_block(db, block_id)
