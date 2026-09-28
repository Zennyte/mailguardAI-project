from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import report_repository
from app.schemas.report import ReportCreateRequest, ReportResponse, ReportPreviewResponse

REPORT_TYPES = ["scan_summary", "label_distribution", "phishing_activity"]
VALID_LABELS = ["safe", "spam", "phishing"]


# Gjeneron te dhenat e raportit sipas llojit (summary/distribution/phishing)
def build_report_data(db: Session, user_id: int, report_type: str,
                      date_from=None, date_to=None, label=None) -> dict:
    if report_type not in REPORT_TYPES:
        raise HTTPException(status_code=400,
                            detail=f"Unknown report type. Allowed: {', '.join(REPORT_TYPES)}")
    if label and label not in VALID_LABELS:
        raise HTTPException(status_code=400, detail="Label must be safe, spam or phishing.")

    stats = report_repository.get_label_stats(db, user_id, date_from, date_to, label)
    counts = {row[0]: row[1] for row in stats}
    averages = {row[0]: float(row[2]) for row in stats}
    total = sum(counts.values())

    # Besueshmeria mesatare e te gjitha skanimeve se bashku
    overall_avg = 0.0
    if total > 0:
        overall_avg = sum(counts[l] * averages[l] for l in counts) / total

    if report_type == "scan_summary":
        return {
            "total_scans": total,
            "safe_count": counts.get("safe", 0),
            "spam_count": counts.get("spam", 0),
            "phishing_count": counts.get("phishing", 0),
            "average_confidence": round(overall_avg, 4),
        }

    if report_type == "label_distribution":
        distribution = [
            {
                "label": l,
                "count": counts[l],
                "percentage": round(counts[l] * 100 / total, 1) if total else 0,
            }
            for l in VALID_LABELS if l in counts
        ]
        return {"total_scans": total, "distribution": distribution}

    # phishing_activity
    phishing_count = counts.get("phishing", 0)
    last_phishing = report_repository.get_latest_scan_date(
        db, user_id, date_from, date_to, "phishing")
    return {
        "total_scans": total,
        "phishing_count": phishing_count,
        "phishing_percentage": round(phishing_count * 100 / total, 1) if total else 0,
        "average_phishing_confidence": round(averages.get("phishing", 0), 4),
        "last_phishing_at": str(last_phishing) if last_phishing else None,
    }


# Kthen te dhena raporti pa i ruajtur ne DB
def preview_report(db: Session, user_id: int, report_type: str,
                   date_from=None, date_to=None, label=None) -> ReportPreviewResponse:
    data = build_report_data(db, user_id, report_type, date_from, date_to, label)
    return ReportPreviewResponse(report_type=report_type, date_from=date_from,
                                 date_to=date_to, label=label, data=data)


# Ruan nje raport te ri bashke me filtrat e perdorur
def create_report(db: Session, user_id: int, request: ReportCreateRequest) -> ReportResponse:
    data = build_report_data(db, user_id, request.report_type,
                             request.date_from, request.date_to, request.label)

    # Raporti ruhet bashke me filtrat e perdorur
    report = report_repository.create_report(db, user_id, request.report_name, request.report_type)
    if request.date_from:
        report_repository.add_filter(db, report.id, "date_from", str(request.date_from))
    if request.date_to:
        report_repository.add_filter(db, report.id, "date_to", str(request.date_to))
    if request.label:
        report_repository.add_filter(db, report.id, "label", request.label)
    db.commit()
    db.refresh(report)

    response = ReportResponse.model_validate(report)
    response.data = data
    return response


# Lista e raporteve te ruajtura te perdoruesit
def list_reports(db: Session, user_id: int) -> list:
    reports = report_repository.get_reports_for_user(db, user_id)
    return [ReportResponse.model_validate(r) for r in reports]


# Rilexon filtrat e ruajtur dhe rigjeneron raportin live
def get_report(db: Session, user_id: int, report_id: int) -> ReportResponse:
    report = report_repository.get_report_for_user(db, report_id, user_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    # Te dhenat rigjenerohen nga filtrat e ruajtur - keshtu raporti eshte dinamik
    filters = {f.filter_key: f.filter_value for f in report.filters}
    date_from = date.fromisoformat(filters["date_from"]) if filters.get("date_from") else None
    date_to = date.fromisoformat(filters["date_to"]) if filters.get("date_to") else None

    response = ReportResponse.model_validate(report)
    response.data = build_report_data(db, user_id, report.report_type,
                                      date_from, date_to, filters.get("label"))
    return response
