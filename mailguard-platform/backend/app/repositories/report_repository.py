from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Report, ReportFilter, ScanRequest, ScanResult


def create_report(db: Session, user_id: int, report_name: str, report_type: str) -> Report:
    report = Report(user_id=user_id, report_name=report_name, report_type=report_type)
    db.add(report)
    db.flush()
    return report


def add_filter(db: Session, report_id: int, key: str, value: str):
    db.add(ReportFilter(report_id=report_id, filter_key=key, filter_value=value))


def get_reports_for_user(db: Session, user_id: int):
    return (
        db.query(Report)
        .filter(Report.user_id == user_id)
        .order_by(Report.id.desc())
        .all()
    )


def get_report_for_user(db: Session, report_id: int, user_id: int):
    return (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == user_id)
        .first()
    )


def _scan_query(db: Session, user_id: int, date_from, date_to, label):
    # Baza e perbashket per te gjitha raportet: skanimet e perdoruesit me filtra
    query = (
        db.query(ScanResult)
        .join(ScanRequest, ScanRequest.id == ScanResult.scan_request_id)
        .filter(ScanRequest.user_id == user_id)
    )
    if date_from:
        query = query.filter(ScanRequest.created_at >= date_from)
    if date_to:
        query = query.filter(ScanRequest.created_at < date_to + timedelta(days=1))
    if label:
        query = query.filter(ScanResult.predicted_label == label)
    return query


def get_label_stats(db: Session, user_id: int, date_from, date_to, label) -> list:
    # Kthen (etikete, numri, besueshmeria mesatare) per cdo etikete
    return (
        _scan_query(db, user_id, date_from, date_to, label)
        .with_entities(
            ScanResult.predicted_label,
            func.count(ScanResult.id),
            func.avg(ScanResult.confidence_score),
        )
        .group_by(ScanResult.predicted_label)
        .all()
    )


def get_latest_scan_date(db: Session, user_id: int, date_from, date_to, label):
    return (
        _scan_query(db, user_id, date_from, date_to, label)
        .with_entities(func.max(ScanRequest.created_at))
        .scalar()
    )
