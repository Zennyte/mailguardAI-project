from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import notification_repository
from app.schemas.notification import NotificationResponse
from app.websockets.notification_connections import notification_connections


# Pas cdo skanimi: njoftimi ruhet ne databaze dhe dergohet live te kambana (WebSocket)
async def notify_scan_completed(db: Session, user_id: int,
                                predicted_label: str, confidence_score: float):
    confidence_percent = round(confidence_score * 100)
    notification = notification_repository.create_notification(
        db,
        user_id,
        title="Email scan completed",
        message=f"The email was classified as {predicted_label} with {confidence_percent}% confidence.",
        notification_type="scan_completed",
    )

    # Dergohet ne te njejten forme si GET /notifications, qe frontend-i ta shtoje direkt ne liste
    live_message = NotificationResponse.model_validate(notification).model_dump(mode="json")
    await notification_connections.send_to_user(user_id, live_message)


def get_notifications_of_user(db: Session, user_id: int) -> list:
    notifications = notification_repository.get_notifications_of_user(db, user_id)
    return [NotificationResponse.model_validate(notification) for notification in notifications]


def mark_notification_as_read(db: Session, user_id: int, notification_id: int) -> NotificationResponse:
    notification = notification_repository.mark_notification_as_read(db, notification_id, user_id)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return NotificationResponse.model_validate(notification)
