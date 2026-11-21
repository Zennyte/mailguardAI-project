from datetime import timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import (
    ScanRequest, ScanResult, EmailMessage, Notification, Report, CmsPage,
)
from app.schemas.search import SearchFilters

# Nje funksion kerkimi per secilen nga 5 listat e faqes Search.
# Te gjitha ndjekin te njejtat hapa: teksti -> datat -> renditja -> limiti.
# Tre funksionet e para te meposhtme jane hapat e perbashket.


# Mban vetem rreshtat ku njeri nga "columns" permban tekstin e kerkuar
def filter_by_text(query, search_text, *columns):
    if not search_text:
        return query
    text_pattern = f"%{search_text}%"
    return query.filter(or_(*[column.ilike(text_pattern) for column in columns]))


# Mban vetem rreshtat e krijuar brenda intervalit [date_from, date_to]
def filter_by_created_date(query, created_at_column, filters: SearchFilters):
    if filters.date_from:
        query = query.filter(created_at_column >= filters.date_from)
    if filters.date_to:
        # Dita e fundit perfshihet e gjitha (deri ne mesnate)
        query = query.filter(created_at_column < filters.date_to + timedelta(days=1))
    return query


# Rendit sipas id-se (id me e madhe = rresht me i ri) dhe merr deri ne "limit" rreshta
def sort_and_limit(query, id_column, filters: SearchFilters):
    if filters.newest_first:
        query = query.order_by(id_column.desc())
    else:
        query = query.order_by(id_column.asc())
    return query.limit(filters.limit).all()


def search_scans(db: Session, user_id: int, filters: SearchFilters):
    query = (
        db.query(ScanRequest)
        .join(ScanResult, ScanResult.scan_request_id == ScanRequest.id)
        .outerjoin(EmailMessage, EmailMessage.id == ScanRequest.email_message_id)
        .filter(ScanRequest.user_id == user_id)
    )
    query = filter_by_text(query, filters.search_text, EmailMessage.subject, EmailMessage.body_preview)
    if filters.label:
        query = query.filter(ScanResult.predicted_label == filters.label)
    query = filter_by_created_date(query, ScanRequest.created_at, filters)
    return sort_and_limit(query, ScanRequest.id, filters)


def search_email_messages(db: Session, user_id: int, filters: SearchFilters):
    query = db.query(EmailMessage).filter(EmailMessage.user_id == user_id)
    query = filter_by_text(query, filters.search_text, EmailMessage.subject, EmailMessage.body_preview)
    query = filter_by_created_date(query, EmailMessage.created_at, filters)
    return sort_and_limit(query, EmailMessage.id, filters)


def search_notifications(db: Session, user_id: int, filters: SearchFilters):
    query = db.query(Notification).filter(Notification.user_id == user_id)
    query = filter_by_text(query, filters.search_text, Notification.title, Notification.message)
    query = filter_by_created_date(query, Notification.created_at, filters)
    return sort_and_limit(query, Notification.id, filters)


def search_reports(db: Session, user_id: int, filters: SearchFilters):
    query = db.query(Report).filter(Report.user_id == user_id)
    query = filter_by_text(query, filters.search_text, Report.report_name, Report.report_type)
    query = filter_by_created_date(query, Report.created_at, filters)
    return sort_and_limit(query, Report.id, filters)


# Faqet CMS jane publike, prandaj kerkohen vetem ato te publikuara (pa user_id)
def search_published_cms_pages(db: Session, filters: SearchFilters):
    query = db.query(CmsPage).filter(CmsPage.is_published == True)  # noqa: E712
    query = filter_by_text(query, filters.search_text, CmsPage.title, CmsPage.slug)
    query = filter_by_created_date(query, CmsPage.created_at, filters)
    return sort_and_limit(query, CmsPage.id, filters)
