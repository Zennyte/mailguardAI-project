# Faqet: Scanner (/scanner), History (/history) dhe Dashboard (/dashboard)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth_dependencies import get_current_user
from app.core.database import get_db
from app.models import User
from app.schemas.scan import (
    ScanEmailRequest, ScanResultResponse, ScanHistoryItem, ScanStatsResponse,
)
from app.services import scan_service

router = APIRouter(prefix="/scans", tags=["Scans"])


# POST /scans/analyze - skanon nje email me modelin ML (butoni "Scan Email")
@router.post("/analyze", response_model=ScanResultResponse)
async def scan_email(
    email: ScanEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await scan_service.scan_email(db, current_user.id, email)


# GET /scans - tabela e faqes History
@router.get("", response_model=list[ScanHistoryItem])
def get_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_scan_history(db, current_user.id)


# GET /scans/stats - kartat e faqes Dashboard
@router.get("/stats", response_model=ScanStatsResponse)
def get_scan_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_scan_stats(db, current_user.id)
