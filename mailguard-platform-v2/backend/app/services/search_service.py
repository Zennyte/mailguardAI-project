from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import search_repository
from app.schemas.search import SearchFilters, SearchResponse

# Listat qe mund te kerkohen (faqja Search) dhe te eksportohen (faqja Import/Export)
SEARCHABLE_LISTS = ["scans", "email_messages", "notifications", "reports", "cms_pages"]


def search(db: Session, user_id: int, list_name: str, filters: SearchFilters) -> SearchResponse:
    rows = find_rows(db, user_id, list_name, filters)
    return SearchResponse(list_name=list_name, count=len(rows), rows=rows)


# Kthen rreshtat e nje liste si dict te thjeshte. Celesat e dict-it behen
# kolonat e tabeles ne faqen Search dhe kolonat e skedarit te eksportuar.
def find_rows(db: Session, user_id: int, list_name: str, filters: SearchFilters) -> list:
    if list_name not in SEARCHABLE_LISTS:
        raise HTTPException(status_code=400,
                            detail=f"Unknown list. Allowed: {', '.join(SEARCHABLE_LISTS)}")

    if list_name == "scans":
        scan_requests = search_repository.search_scans(db, user_id, filters)
        return [{
            "scan_request_id": scan_request.id,
            "subject": scan_request.email_message.subject if scan_request.email_message else None,
            "predicted_label": scan_request.result.predicted_label,
            "confidence_score": float(scan_request.result.confidence_score),
            "status": scan_request.status,
            "created_at": scan_request.created_at,
        } for scan_request in scan_requests]

    if list_name == "email_messages":
        email_messages = search_repository.search_email_messages(db, user_id, filters)
        return [{
            "id": email_message.id,
            "subject": email_message.subject,
            "body_preview": email_message.body_preview,
            "source_type": email_message.source_type,
            "created_at": email_message.created_at,
        } for email_message in email_messages]

    if list_name == "notifications":
        notifications = search_repository.search_notifications(db, user_id, filters)
        return [{
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "notification_type": notification.notification_type,
            "is_read": notification.is_read,
            "created_at": notification.created_at,
        } for notification in notifications]

    if list_name == "reports":
        reports = search_repository.search_reports(db, user_id, filters)
        return [{
            "id": report.id,
            "report_name": report.report_name,
            "report_type": report.report_type,
            "created_at": report.created_at,
        } for report in reports]

    # list_name == "cms_pages"
    cms_pages = search_repository.search_published_cms_pages(db, filters)
    return [{
        "id": cms_page.id,
        "title": cms_page.title,
        "slug": cms_page.slug,
        "is_published": cms_page.is_published,
        "created_at": cms_page.created_at,
    } for cms_page in cms_pages]
