import csv
import io
import json
from datetime import date

from fastapi import HTTPException
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.models import ExportJob
from app.schemas.search import SearchFilters
from app.services import search_service

# Formati i skedarit -> lloji i permbajtjes (Content-Type) qe i tregohet shfletuesit
CONTENT_TYPE_PER_FORMAT = {
    "csv": "text/csv",
    "json": "application/json",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}

MAX_EXPORTED_ROWS = 10000


# Butoni "Export" ne faqen Import/Export.
# Kthen tri gjera: permbajtjen e skedarit, llojin e permbajtjes dhe emrin e skedarit.
def export_list(db: Session, user_id: int, list_name: str, file_format: str):
    if file_format not in CONTENT_TYPE_PER_FORMAT:
        raise HTTPException(status_code=400,
                            detail=f"Unknown format. Allowed: {', '.join(CONTENT_TYPE_PER_FORMAT)}")

    # Eksportohen te njejtat rreshta qe kthen kerkimi, por pa filtra
    rows = search_service.find_rows(db, user_id, list_name, SearchFilters(limit=MAX_EXPORTED_ROWS))

    if file_format == "csv":
        file_content = rows_to_csv(rows)
    elif file_format == "json":
        file_content = rows_to_json(rows)
    else:
        file_content = rows_to_xlsx(rows)

    # Regjistrojme eksportin ne tabelen export_jobs
    db.add(ExportJob(user_id=user_id, export_type=file_format, status="completed"))
    db.commit()

    file_name = f"{list_name}_{date.today()}.{file_format}"
    return file_content, CONTENT_TYPE_PER_FORMAT[file_format], file_name


def rows_to_csv(rows: list) -> bytes:
    csv_text = io.StringIO()
    if rows:
        csv_writer = csv.DictWriter(csv_text, fieldnames=rows[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(rows)
    # utf-8-sig qe Excel t'i lexoje sakte shkronjat speciale
    return csv_text.getvalue().encode("utf-8-sig")


def rows_to_json(rows: list) -> bytes:
    # default=str i kthen datat ne tekst
    return json.dumps(rows, indent=2, default=str).encode("utf-8")


def rows_to_xlsx(rows: list) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    if rows:
        sheet.append(list(rows[0].keys()))
        for row in rows:
            sheet.append([str(value) if value is not None else "" for value in row.values()])
    xlsx_bytes = io.BytesIO()
    workbook.save(xlsx_bytes)
    return xlsx_bytes.getvalue()
