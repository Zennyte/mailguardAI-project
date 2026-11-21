from sqlalchemy.orm import Session

from app.models import Notification


def create_notification(db: Session, user_id: int, title: str, message: str,
                        notification_type: str) -> Notification:
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# Njoftimet e nje perdoruesi, me te rejat te parat
def get_notifications_of_user(db: Session, user_id: int, limit: int = 50):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.id.desc())
        .limit(limit)
        .all()
    )


# Perdoruesi mund te shenoje si te lexuara vetem njoftimet e veta.
# Kthen None nese njoftimi nuk ekziston ose eshte i dikujt tjeter.
def mark_notification_as_read(db: Session, notification_id: int, user_id: int):
    notification = (
        db.query(Notification)
        .filter(Notification.id == notification_id, Notification.user_id == user_id)
        .first()
    )
    if notification is None:
        return None
    notification.is_read = True
    db.commit()
    db.refresh(notification)
    return notification
