from datetime import timedelta

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Report, ReportFilter, ScanRequest, ScanResult


# ---------- Raportet e ruajtura (lista "Saved reports") ----------

# Shton raportin pa bere commit - service shton edhe filtrat dhe ben commit ne fund
def add_report(db: Session, user_id: int, report_name: str, report_type: str) -> Report:
    report = Report(user_id=user_id, report_name=report_name, report_type=report_type)
    db.add(report)
    db.flush()  # flush na jep id-ne e raportit per filtrat
    return report


def add_report_filter(db: Session, report_id: int, filter_key: str, filter_value: str):
    db.add(ReportFilter(report_id=report_id, filter_key=filter_key, filter_value=filter_value))


def get_reports_of_user(db: Session, user_id: int):
    return (
        db.query(Report)
        .filter(Report.user_id == user_id)
        .order_by(Report.id.desc())
        .all()
    )


def find_report_of_user(db: Session, report_id: int, user_id: int):
    return (
        db.query(Report)
        .filter(Report.id == report_id, Report.user_id == user_id)
        .first()
    )


# ---------- Numrat e raportit (llogariten nga skanimet) ----------

# Baza e perbashket e te gjitha raporteve: skanimet e perdoruesit, te filtruara
def filtered_scan_results(db: Session, user_id: int, date_from, date_to, label):
    query = (
        db.query(ScanResult)
        .join(ScanRequest, ScanRequest.id == ScanResult.scan_request_id)
        .filter(ScanRequest.user_id == user_id)
    )
    if date_from:
        query = query.filter(ScanRequest.created_at >= date_from)
    if date_to:
        # Dita e fundit perfshihet e gjitha (deri ne mesnate)
        query = query.filter(ScanRequest.created_at < date_to + timedelta(days=1))
    if label:
        query = query.filter(ScanResult.predicted_label == label)
    return query


# Nje rresht per cdo etikete: (etiketa, numri i skanimeve, besueshmeria mesatare)
def get_count_and_average_confidence_per_label(db: Session, user_id: int,
                                               date_from, date_to, label) -> list:
    return (
        filtered_scan_results(db, user_id, date_from, date_to, label)
        .with_entities(
            ScanResult.predicted_label,
            func.count(ScanResult.id),
            func.avg(ScanResult.confidence_score),
        )
        .group_by(ScanResult.predicted_label)
        .all()
    )


# Data e skanimit te fundit phishing (None nese nuk ka asnje)
def get_latest_phishing_scan_date(db: Session, user_id: int, date_from, date_to):
    return (
        filtered_scan_results(db, user_id, date_from, date_to, "phishing")
        .with_entities(func.max(ScanRequest.created_at))
        .scalar()
    )
