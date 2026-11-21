# Faqja: Reports (/reports)
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_dependencies import get_current_user
from app.models import User
from app.schemas.report import ReportCreateRequest, ReportResponse, ReportPreviewResponse
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])


# POST /reports - butoni "Save Report"
@router.post("", response_model=ReportResponse, status_code=201)
def save_report(
    form: ReportCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.save_report(db, current_user.id, form)


# GET /reports - lista "Saved reports"
@router.get("", response_model=list[ReportResponse])
def get_saved_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.get_saved_reports(db, current_user.id)


# GET /reports/preview - butoni "Preview" (nuk ruan asgje)
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


# GET /reports/{id} - butoni "View" i nje raporti te ruajtur
@router.get("/{report_id}", response_model=ReportResponse)
def open_saved_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return report_service.open_saved_report(db, current_user.id, report_id)
