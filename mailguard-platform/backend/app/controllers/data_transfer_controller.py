from fastapi import APIRouter, Depends, File, Response, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models import User
from app.schemas.data_transfer import ImportSummary
from app.services import export_service, import_service

router = APIRouter(prefix="/data", tags=["Import/Export"])


@router.get("/export/{entity}")
def export_data(
    entity: str,
    format: str = "csv",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content, media_type, filename = export_service.export_entity(
        db, current_user.id, entity, format,
    )
    return Response(
        content=content,
        media_type=media_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/import/{entity}", response_model=ImportSummary)
async def import_data(
    entity: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    content = await file.read()
    return import_service.import_entity(db, current_user.id, entity, file.filename, content)
