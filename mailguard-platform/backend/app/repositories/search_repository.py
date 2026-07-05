from datetime import timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models import (
    ScanRequest, ScanResult, EmailMessage, Notification, Report, CmsPage,
)


def _apply_dates(query, column, date_from, date_to):
    if date_from:
        query = query.filter(column >= date_from)
    if date_to:
        # date_to perfshihet i gjithe (deri ne fund te dites)
        query = query.filter(column < date_to + timedelta(days=1))
    return query


def _apply_sort(query, column, sort_order):
    return query.order_by(column.desc() if sort_order == "desc" else column.asc())


def search_scans(db: Session, user_id: int, q, label, status,
                 date_from, date_to, sort_by, sort_order, limit):
    query = (
        db.query(ScanRequest)
        .join(ScanResult, ScanResult.scan_request_id == ScanRequest.id)
        .outerjoin(EmailMessage, EmailMessage.id == ScanRequest.email_message_id)
        .filter(ScanRequest.user_id == user_id)
    )
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(
            EmailMessage.subject.ilike(pattern),
            EmailMessage.body_preview.ilike(pattern),
        ))
    if label:
        query = query.filter(ScanResult.predicted_label == label)
    if status:
        query = query.filter(ScanRequest.status == status)
    query = _apply_dates(query, ScanRequest.created_at, date_from, date_to)
    column = ScanRequest.id if sort_by == "id" else ScanRequest.created_at
    return _apply_sort(query, column, sort_order).limit(limit).all()


def search_email_messages(db: Session, user_id: int, q,
                          date_from, date_to, sort_by, sort_order, limit):
    query = db.query(EmailMessage).filter(EmailMessage.user_id == user_id)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(
            EmailMessage.subject.ilike(pattern),
            EmailMessage.body_preview.ilike(pattern),
        ))
    query = _apply_dates(query, EmailMessage.created_at, date_from, date_to)
    column = EmailMessage.id if sort_by == "id" else EmailMessage.created_at
    return _apply_sort(query, column, sort_order).limit(limit).all()


def search_notifications(db: Session, user_id: int, q,
                         date_from, date_to, sort_by, sort_order, limit):
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(
            Notification.title.ilike(pattern),
            Notification.message.ilike(pattern),
        ))
    query = _apply_dates(query, Notification.created_at, date_from, date_to)
    column = Notification.id if sort_by == "id" else Notification.created_at
    return _apply_sort(query, column, sort_order).limit(limit).all()


def search_reports(db: Session, user_id: int, q,
                   date_from, date_to, sort_by, sort_order, limit):
    query = db.query(Report).filter(Report.user_id == user_id)
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(
            Report.report_name.ilike(pattern),
            Report.report_type.ilike(pattern),
        ))
    query = _apply_dates(query, Report.created_at, date_from, date_to)
    column = Report.id if sort_by == "id" else Report.created_at
    return _apply_sort(query, column, sort_order).limit(limit).all()


def search_cms_pages(db: Session, q, date_from, date_to, sort_by, sort_order, limit):
    # Faqet CMS jane publike - kerkohen vetem ato te publikuara
    query = db.query(CmsPage).filter(CmsPage.is_published == True)  # noqa: E712
    if q:
        pattern = f"%{q}%"
        query = query.filter(or_(
            CmsPage.title.ilike(pattern),
            CmsPage.slug.ilike(pattern),
        ))
    query = _apply_dates(query, CmsPage.created_at, date_from, date_to)
    column = CmsPage.id if sort_by == "id" else CmsPage.created_at
    return _apply_sort(query, column, sort_order).limit(limit).all()
