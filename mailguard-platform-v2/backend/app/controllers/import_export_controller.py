# Faqja: Import/Export (/import-export)
from fastapi import APIRouter, Depends, File, Response, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_dependencies import require_permission
from app.models import User
from app.schemas.import_export import ImportSummary
from app.services import export_service, import_service

router = APIRouter(prefix="/data", tags=["Import/Export"])


# GET /data/export/{list_name}?file_format=csv - shkarkon nje liste si CSV/JSON/XLSX
@router.get("/export/{list_name}")
def export_list(
    list_name: str,
    file_format: str = "csv",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("export_data")),
):
    file_content, content_type, file_name = export_service.export_list(
        db, current_user.id, list_name, file_format,
    )
    return Response(
        content=file_content,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
    )


# POST /data/import/{list_name} - importon rreshta nga nje skedar i ngarkuar
@router.post("/import/{list_name}", response_model=ImportSummary)
async def import_list(
    list_name: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("import_data")),
):
    file_content = await file.read()
    return import_service.import_list(db, current_user.id, list_name, file.filename, file_content)
