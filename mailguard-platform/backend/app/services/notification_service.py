from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import notification_repository
from app.schemas.notification import NotificationResponse
from app.websockets.connection_manager import manager


async def notify_scan_completed(db: Session, user_id: int,
                                predicted_label: str, confidence_score: float):
    title = "Email scan completed"
    confidence_percent = round(confidence_score * 100)
    message = f"The email was classified as {predicted_label} with {confidence_percent}% confidence."

    notification = notification_repository.create(db, user_id, title, message, "scan_completed")

    # Dergimi i njoftimit live pas analizimit
    await manager.send_to_user(user_id, {
        "id": notification.id,
        "type": notification.notification_type,
        "title": notification.title,
        "message": notification.message,
        "created_at": str(notification.created_at),
    })
    return notification


def list_for_user(db: Session, user_id: int) -> list:
    notifications = notification_repository.get_for_user(db, user_id)
    return [NotificationResponse.model_validate(n) for n in notifications]


def mark_as_read(db: Session, user_id: int, notification_id: int) -> NotificationResponse:
    notification = notification_repository.mark_read(db, notification_id, user_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse.model_validate(notification)
