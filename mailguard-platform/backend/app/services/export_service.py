import csv
import io
import json
from datetime import date

from fastapi import HTTPException
from openpyxl import Workbook
from sqlalchemy.orm import Session

from app.services import search_service

EXPORT_FORMATS = ["csv", "json", "xlsx"]

MEDIA_TYPES = {
    "csv": "text/csv",
    "json": "application/json",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
}


# Eksporton nje liste te dhenash ne formatin e kerkuar
def export_entity(db: Session, user_id: int, entity: str, format: str):
    if format not in EXPORT_FORMATS:
        raise HTTPException(status_code=400,
                            detail=f"Unknown format. Allowed: {', '.join(EXPORT_FORMATS)}")

    # Eksportohen te njejtat te dhena qe kthen kerkimi (pa filtra)
    rows = search_service.get_rows(db, user_id, entity, limit=10000)

    if format == "csv":
        content = _to_csv(rows)
    elif format == "json":
        content = _to_json(rows)
    else:
        content = _to_xlsx(rows)

    filename = f"{entity}_{date.today()}.{format}"
    return content, MEDIA_TYPES[format], filename


# Konverton rreshtat ne CSV
def _to_csv(rows: list) -> bytes:
    output = io.StringIO()
    if rows:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return output.getvalue().encode("utf-8-sig")


# Konverton rreshtat ne JSON
def _to_json(rows: list) -> bytes:
    # default=str kthen datat ne tekst
    return json.dumps(rows, indent=2, default=str).encode("utf-8")


# Konverton rreshtat ne nje skedar Excel
def _to_xlsx(rows: list) -> bytes:
    workbook = Workbook()
    sheet = workbook.active
    if rows:
        sheet.append(list(rows[0].keys()))
        for row in rows:
            sheet.append([str(v) if v is not None else "" for v in row.values()])
    output = io.BytesIO()
    workbook.save(output)
    return output.getvalue()
