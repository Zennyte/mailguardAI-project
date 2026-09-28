from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.scan import (
    ScanEmailRequest, ScanResultResponse, ScanHistoryItem, ScanStatsResponse,
)
from app.services import scan_service

router = APIRouter(prefix="/scans", tags=["Scans"])


# POST /scans/analyze - skanon nje email me modelin ML
@router.post("/analyze", response_model=ScanResultResponse)
async def analyze_email(
    data: ScanEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await scan_service.analyze_email(db, current_user.id, data)


# GET /scans - historiku i skanimeve te perdoruesit
@router.get("", response_model=list[ScanHistoryItem])
def get_scan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_history(db, current_user.id)


# Kujdes: "/stats" duhet te deklarohet para "/{scan_request_id}"
@router.get("/stats", response_model=ScanStatsResponse)
def get_scan_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_stats(db, current_user.id)


# GET /scans/{id} - detajet e nje skanimi specifik
@router.get("/{scan_request_id}", response_model=ScanResultResponse)
def get_scan(
    scan_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_scan(db, current_user.id, scan_request_id)
