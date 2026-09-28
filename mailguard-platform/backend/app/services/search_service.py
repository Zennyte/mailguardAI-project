from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import search_repository
from app.schemas.search import SearchResponse

ALLOWED_ENTITIES = ["scans", "email_messages", "notifications", "reports", "cms_pages"]


# Kerkon dhe e mbeshtjell rezultatin ne SearchResponse
def search(db: Session, user_id: int, entity: str, q=None, label=None, status=None,
           date_from=None, date_to=None, sort_by="created_at",
           sort_order="desc", limit=50) -> SearchResponse:
    results = get_rows(db, user_id, entity, q, label, status,
                       date_from, date_to, sort_by, sort_order, limit)
    return SearchResponse(entity=entity, count=len(results), results=results)


# Thërret repository-n e duhur sipas listes (entity) dhe formaton rreshtat
def get_rows(db: Session, user_id: int, entity: str, q=None, label=None, status=None,
             date_from=None, date_to=None, sort_by="created_at",
             sort_order="desc", limit=50) -> list:
    # Lejohen vetem listat e njohura
    if entity not in ALLOWED_ENTITIES:
        raise HTTPException(status_code=400,
                            detail=f"Unknown entity. Allowed: {', '.join(ALLOWED_ENTITIES)}")

    if entity == "scans":
        rows = search_repository.search_scans(
            db, user_id, q, label, status, date_from, date_to, sort_by, sort_order, limit)
        return [{
            "scan_request_id": r.id,
            "subject": r.email_message.subject if r.email_message else None,
            "predicted_label": r.result.predicted_label if r.result else None,
            "confidence_score": float(r.result.confidence_score) if r.result else None,
            "status": r.status,
            "created_at": r.created_at,
        } for r in rows]

    if entity == "email_messages":
        rows = search_repository.search_email_messages(
            db, user_id, q, date_from, date_to, sort_by, sort_order, limit)
        return [{
            "id": r.id,
            "subject": r.subject,
            "body_preview": r.body_preview,
            "source_type": r.source_type,
            "created_at": r.created_at,
        } for r in rows]

    if entity == "notifications":
        rows = search_repository.search_notifications(
            db, user_id, q, date_from, date_to, sort_by, sort_order, limit)
        return [{
            "id": r.id,
            "title": r.title,
            "message": r.message,
            "notification_type": r.notification_type,
            "is_read": r.is_read,
            "created_at": r.created_at,
        } for r in rows]

    if entity == "reports":
        rows = search_repository.search_reports(
            db, user_id, q, date_from, date_to, sort_by, sort_order, limit)
        return [{
            "id": r.id,
            "report_name": r.report_name,
            "report_type": r.report_type,
            "created_at": r.created_at,
        } for r in rows]

    # cms_pages
    rows = search_repository.search_cms_pages(
        db, q, date_from, date_to, sort_by, sort_order, limit)
    return [{
        "id": r.id,
        "title": r.title,
        "slug": r.slug,
        "is_published": r.is_published,
        "created_at": r.created_at,
    } for r in rows]
