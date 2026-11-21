# Kambana e njoftimeve (lart djathtas, ne cdo faqe pas kycjes)
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth_dependencies import get_current_user
from app.models import User
from app.schemas.notification import NotificationResponse
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# GET /notifications - lista qe hapet kur klikohet kambana
@router.get("", response_model=list[NotificationResponse])
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_service.get_notifications_of_user(db, current_user.id)


# PATCH /notifications/{id}/read - linku "Mark as read"
@router.patch("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return notification_service.mark_notification_as_read(db, current_user.id, notification_id)
