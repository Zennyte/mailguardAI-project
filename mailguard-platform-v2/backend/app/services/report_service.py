from datetime import date

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.constants import EMAIL_LABELS
from app.repositories import report_repository
from app.schemas.report import ReportCreateRequest, ReportResponse, ReportPreviewResponse

# Tri llojet e raporteve ne dropdown-in "Report type" te faqes Reports
REPORT_TYPES = ["scan_summary", "label_distribution", "phishing_activity"]


# Llogarit numrat e nje raporti nga skanimet e perdoruesit.
# Thirret nga Preview, Save Report dhe View - keshtu raporti eshte gjithmone i fresket.
def build_report_data(db: Session, user_id: int, report_type: str,
                      date_from=None, date_to=None, label=None) -> dict:
    if report_type not in REPORT_TYPES:
        raise HTTPException(status_code=400,
                            detail=f"Unknown report type. Allowed: {', '.join(REPORT_TYPES)}")
    if label and label not in EMAIL_LABELS:
        raise HTTPException(status_code=400, detail="Label must be safe, spam or phishing.")

    # Nga databaza vjen nje rresht per etikete: (etiketa, numri, besueshmeria mesatare)
    rows_per_label = report_repository.get_count_and_average_confidence_per_label(
        db, user_id, date_from, date_to, label)

    scan_count_per_label = {}
    average_confidence_per_label = {}
    for row_label, scan_count, average_confidence in rows_per_label:
        scan_count_per_label[row_label] = scan_count
        average_confidence_per_label[row_label] = float(average_confidence)

    total_scans = sum(scan_count_per_label.values())

    if report_type == "scan_summary":
        return build_scan_summary(total_scans, scan_count_per_label, average_confidence_per_label)

    if report_type == "label_distribution":
        return build_label_distribution(total_scans, scan_count_per_label)

    latest_phishing_date = report_repository.get_latest_phishing_scan_date(
        db, user_id, date_from, date_to)
    return build_phishing_activity(total_scans, scan_count_per_label,
                                   average_confidence_per_label, latest_phishing_date)


# Raporti "Scan Summary": sa skanime gjithsej dhe per cdo etikete
def build_scan_summary(total_scans: int, scan_count_per_label: dict,
                       average_confidence_per_label: dict) -> dict:
    # Besueshmeria mesatare e te gjitha skanimeve se bashku
    average_confidence = 0.0
    if total_scans > 0:
        confidence_sum = 0.0
        for label, scan_count in scan_count_per_label.items():
            confidence_sum += scan_count * average_confidence_per_label[label]
        average_confidence = confidence_sum / total_scans

    return {
        "total_scans": total_scans,
        "safe_count": scan_count_per_label.get("safe", 0),
        "spam_count": scan_count_per_label.get("spam", 0),
        "phishing_count": scan_count_per_label.get("phishing", 0),
        "average_confidence": round(average_confidence, 4),
    }


# Raporti "Label Distribution": sa perqind e skanimeve i takon cdo etikete
def build_label_distribution(total_scans: int, scan_count_per_label: dict) -> dict:
    distribution = []
    for label in EMAIL_LABELS:
        if label in scan_count_per_label:
            scan_count = scan_count_per_label[label]
            distribution.append({
                "label": label,
                "count": scan_count,
                "percentage": round(scan_count * 100 / total_scans, 1),
            })
    return {"total_scans": total_scans, "distribution": distribution}


# Raporti "Phishing Activity": sa shpesh dhe kur u gjet phishing
def build_phishing_activity(total_scans: int, scan_count_per_label: dict,
                            average_confidence_per_label: dict, latest_phishing_date) -> dict:
    phishing_count = scan_count_per_label.get("phishing", 0)
    phishing_percentage = round(phishing_count * 100 / total_scans, 1) if total_scans else 0
    return {
        "total_scans": total_scans,
        "phishing_count": phishing_count,
        "phishing_percentage": phishing_percentage,
        "average_phishing_confidence": round(average_confidence_per_label.get("phishing", 0), 4),
        "last_phishing_at": str(latest_phishing_date) if latest_phishing_date else None,
    }


# Butoni "Preview": kthen numrat pa ruajtur asgje
def preview_report(db: Session, user_id: int, report_type: str,
                   date_from=None, date_to=None, label=None) -> ReportPreviewResponse:
    report_data = build_report_data(db, user_id, report_type, date_from, date_to, label)
    return ReportPreviewResponse(report_type=report_type, date_from=date_from,
                                 date_to=date_to, label=label, report_data=report_data)


# Butoni "Save Report": ruhen vetem emri, lloji dhe filtrat - jo numrat
def save_report(db: Session, user_id: int, form: ReportCreateRequest) -> ReportResponse:
    report_data = build_report_data(db, user_id, form.report_type,
                                    form.date_from, form.date_to, form.label)

    report = report_repository.add_report(db, user_id, form.report_name, form.report_type)
    if form.date_from:
        report_repository.add_report_filter(db, report.id, "date_from", str(form.date_from))
    if form.date_to:
        report_repository.add_report_filter(db, report.id, "date_to", str(form.date_to))
    if form.label:
        report_repository.add_report_filter(db, report.id, "label", form.label)
    db.commit()
    db.refresh(report)

    response = ReportResponse.model_validate(report)
    response.report_data = report_data
    return response


# Lista "Saved reports" (pa numra - ata llogariten kur hapet raporti)
def get_saved_reports(db: Session, user_id: int) -> list:
    reports = report_repository.get_reports_of_user(db, user_id)
    return [ReportResponse.model_validate(report) for report in reports]


# Butoni "View": lexon filtrat e ruajtur dhe i llogarit numrat nga e para
def open_saved_report(db: Session, user_id: int, report_id: int) -> ReportResponse:
    report = report_repository.find_report_of_user(db, report_id, user_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")

    saved_filters = {}
    for report_filter in report.filters:
        saved_filters[report_filter.filter_key] = report_filter.filter_value

    date_from = date.fromisoformat(saved_filters["date_from"]) if "date_from" in saved_filters else None
    date_to = date.fromisoformat(saved_filters["date_to"]) if "date_to" in saved_filters else None

    response = ReportResponse.model_validate(report)
    response.report_data = build_report_data(db, user_id, report.report_type,
                                             date_from, date_to, saved_filters.get("label"))
    return response
