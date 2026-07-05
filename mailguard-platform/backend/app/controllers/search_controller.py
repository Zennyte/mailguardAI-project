from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.search import SearchResponse
from app.services import search_service

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("", response_model=SearchResponse)
def search(
    entity: str,
    q: str = None,
    label: str = None,
    status: str = None,
    date_from: date = None,
    date_to: date = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return search_service.search(
        db, current_user.id, entity, q, label, status,
        date_from, date_to, sort_by, sort_order, limit,
    )
