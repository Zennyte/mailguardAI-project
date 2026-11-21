import csv
import io
import json

from fastapi import HTTPException
from openpyxl import load_workbook
from sqlalchemy.orm import Session

from app.core.constants import EMAIL_LABELS
from app.models import (
    EmailMessage, CmsPage, UserFeedback, Setting, Notification,
    ImportJob, ScanResult, ScanRequest,
)
from app.schemas.import_export import ImportSummary

# Listat qe mund te importohen ne faqen Import/Export
IMPORTABLE_LISTS = ["email_messages", "cms_pages", "user_feedback", "settings", "notifications"]


# Butoni "Import" ne faqen Import/Export: lexon skedarin dhe shton rreshtat e vlefshem
def import_list(db: Session, user_id: int, list_name: str,
                file_name: str, file_content: bytes) -> ImportSummary:
    if list_name not in IMPORTABLE_LISTS:
        raise HTTPException(status_code=400,
                            detail=f"Unknown list. Allowed: {', '.join(IMPORTABLE_LISTS)}")

    rows = read_rows_from_file(file_name, file_content)

    if list_name == "email_messages":
        imported_count, skipped_count = import_email_messages(db, user_id, rows)
    elif list_name == "cms_pages":
        imported_count, skipped_count = import_cms_pages(db, user_id, rows)
    elif list_name == "user_feedback":
        imported_count, skipped_count = import_user_feedback(db, user_id, rows)
    elif list_name == "settings":
        imported_count, skipped_count = import_settings(db, user_id, rows)
    else:
        imported_count, skipped_count = import_notifications(db, user_id, rows)

    # Regjistrojme importin ne tabelen import_jobs dhe ruajme gjithcka me nje commit
    db.add(ImportJob(user_id=user_id, status="completed",
                     total_rows=len(rows), processed_rows=imported_count))
    db.commit()

    return ImportSummary(
        list_name=list_name,
        imported_count=imported_count,
        skipped_count=skipped_count,
        message=f"Imported {imported_count} rows, skipped {skipped_count} invalid rows.",
    )


# ---------- Leximi i skedarit ----------

# Kthen rreshtat e skedarit si liste dict-esh: [{"subject": "...", "body": "..."}, ...]
# Formati njihet nga prapashtesa e emrit te skedarit.
def read_rows_from_file(file_name: str, file_content: bytes) -> list:
    lowercase_file_name = (file_name or "").lower()
    try:
        if lowercase_file_name.endswith(".csv"):
            csv_text = file_content.decode("utf-8-sig")
            return [dict(row) for row in csv.DictReader(io.StringIO(csv_text))]

        if lowercase_file_name.endswith(".json"):
            rows = json.loads(file_content)
            if not isinstance(rows, list):
                raise ValueError("JSON must be a list of objects")
            return rows

        if lowercase_file_name.endswith(".xlsx"):
            sheet = load_workbook(io.BytesIO(file_content), read_only=True).active
            sheet_rows = sheet.iter_rows(values_only=True)
            # Rreshti i pare i Excel-it permban emrat e kolonave
            column_names = [str(column_name) for column_name in next(sheet_rows, [])]
            return [dict(zip(column_names, sheet_row)) for sheet_row in sheet_rows]
    except Exception:
        raise HTTPException(status_code=400, detail="Could not read the uploaded file.")

    raise HTTPException(status_code=400, detail="Unsupported file type. Use .csv, .json or .xlsx")


# Lexon nje kolone te rreshtit si tekst; kthen "" nese kolona mungon
def read_text_column(row: dict, column_name: str) -> str:
    value = row.get(column_name)
    return str(value).strip() if value is not None else ""


# "true", "1" dhe "yes" numerohen si True, cdo gje tjeter si False
def is_true_value(value) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes")


# ---------- Importi i secilit lloj liste ----------
# Secili funksion kthen (sa rreshta u importuan, sa u anashkaluan)

# Kolonat: subject, body. Rreshtat pa body anashkalohen.
def import_email_messages(db: Session, user_id: int, rows: list):
    imported_count = 0
    skipped_count = 0
    for row in rows:
        body = read_text_column(row, "body")
        if not body:
            skipped_count += 1
            continue
        db.add(EmailMessage(
            user_id=user_id,
            subject=read_text_column(row, "subject")[:500],
            body_preview=body[:500],
            source_type="imported",
        ))
        imported_count += 1
    return imported_count, skipped_count


# Kolonat: title, slug, is_published. Slug-et qe ekzistojne anashkalohen.
def import_cms_pages(db: Session, user_id: int, rows: list):
    imported_count = 0
    skipped_count = 0
    for row in rows:
        title = read_text_column(row, "title")
        slug = read_text_column(row, "slug")
        slug_already_exists = slug and db.query(CmsPage).filter(CmsPage.slug == slug).first()
        if not title or not slug or slug_already_exists:
            skipped_count += 1
            continue
        db.add(CmsPage(
            title=title[:200],
            slug=slug[:200],
            is_published=is_true_value(row.get("is_published")),
            created_by=user_id,
        ))
        db.flush()  # qe slug-u i ri te njihet nga rreshtat pasues
        imported_count += 1
    return imported_count, skipped_count


# Kolonat: scan_result_id, correct_label, comment.
# Feedback lejohet vetem per skanimet e vete perdoruesit.
def import_user_feedback(db: Session, user_id: int, rows: list):
    imported_count = 0
    skipped_count = 0
    for row in rows:
        try:
            scan_result_id = int(row.get("scan_result_id"))
        except (TypeError, ValueError):
            skipped_count += 1
            continue

        own_scan_result = (
            db.query(ScanResult)
            .join(ScanRequest, ScanRequest.id == ScanResult.scan_request_id)
            .filter(ScanResult.id == scan_result_id, ScanRequest.user_id == user_id)
            .first()
        )
        correct_label = read_text_column(row, "correct_label")
        label_is_invalid = correct_label and correct_label not in EMAIL_LABELS
        if own_scan_result is None or label_is_invalid:
            skipped_count += 1
            continue

        db.add(UserFeedback(
            scan_result_id=scan_result_id,
            user_id=user_id,
            correct_label=correct_label or None,
            comment=read_text_column(row, "comment") or None,
        ))
        imported_count += 1
    return imported_count, skipped_count


# Kolonat: key (ose setting_key), value (ose setting_value), description.
# Konfigurimet ekzistuese nuk mbishkruhen.
def import_settings(db: Session, user_id: int, rows: list):
    imported_count = 0
    skipped_count = 0
    for row in rows:
        setting_key = read_text_column(row, "key") or read_text_column(row, "setting_key")
        key_already_exists = setting_key and db.query(Setting).filter(Setting.setting_key == setting_key).first()
        if not setting_key or key_already_exists:
            skipped_count += 1
            continue
        db.add(Setting(
            setting_key=setting_key[:100],
            setting_value=read_text_column(row, "value") or read_text_column(row, "setting_value"),
            description=read_text_column(row, "description")[:255] or None,
            created_by=user_id,
        ))
        db.flush()  # qe celesi i ri te njihet nga rreshtat pasues
        imported_count += 1
    return imported_count, skipped_count


# Kolonat: title, message, type (ose notification_type). Rreshtat pa title anashkalohen.
def import_notifications(db: Session, user_id: int, rows: list):
    imported_count = 0
    skipped_count = 0
    for row in rows:
        title = read_text_column(row, "title")
        if not title:
            skipped_count += 1
            continue
        db.add(Notification(
            user_id=user_id,
            title=title[:200],
            message=read_text_column(row, "message") or None,
            notification_type=(read_text_column(row, "type")
                               or read_text_column(row, "notification_type") or None),
        ))
        imported_count += 1
    return imported_count, skipped_count
