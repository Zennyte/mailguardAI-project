from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.scan import ScanEmailRequest, ScanResultResponse
from app.services import scan_service

router = APIRouter(prefix="/scans", tags=["Scans"])


@router.post("/analyze", response_model=ScanResultResponse)
async def analyze_email(
    data: ScanEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await scan_service.analyze_email(db, current_user.id, data)


@router.get("/{scan_request_id}", response_model=ScanResultResponse)
def get_scan(
    scan_request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return scan_service.get_scan(db, current_user.id, scan_request_id)
