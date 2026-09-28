from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.report import ReportCreateRequest, ReportResponse, ReportPreviewResponse
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


# POST /reports - gjeneron dhe ruan nje raport te ri
@router.post("", response_model=ReportResponse, status_code=201)
def create_report(
    data: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.create_report(db, current_user.id, data)


# GET /reports - lista e raporteve te ruajtura te perdoruesit
@router.get("", response_model=list[ReportResponse])
def list_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.list_reports(db, current_user.id)


# Kujdes: "/preview" duhet te deklarohet para "/{report_id}"
@router.get("/preview", response_model=ReportPreviewResponse)
def preview_report(
    report_type: str = "scan_summary",
    date_from: date = None,
    date_to: date = None,
    label: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.preview_report(
        db, current_user.id, report_type, date_from, date_to, label)


# GET /reports/{id} - rigjeneron nje raport te ruajtur me te dhena te freskta
@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.get_report(db, current_user.id, report_id)
