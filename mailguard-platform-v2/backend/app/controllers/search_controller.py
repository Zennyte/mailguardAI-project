# Faqja: Search (/search)
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_dependencies import get_current_user
from app.models import User
from app.schemas.search import SearchFilters, SearchResponse
from app.services import search_service

router = APIRouter(prefix="/search", tags=["Search"])


# GET /search?list_name=scans&search_text=bank&label=phishing&date_from=2026-01-01
# Nje endpoint i vetem per 5 lista; cdo filter eshte opsional
@router.get("", response_model=SearchResponse)
def search(
    list_name: str,
    search_text: str = None,
    label: str = None,
    date_from: date = None,
    date_to: date = None,
    newest_first: bool = True,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filters = SearchFilters(
        search_text=search_text,
        label=label,
        date_from=date_from,
        date_to=date_to,
        newest_first=newest_first,
        limit=limit,
    )
    return search_service.search(db, current_user.id, list_name, filters)
