from datetime import datetime

from pydantic import BaseModel


# Forma e nje njoftimi ne pergjigjen e API
class NotificationResponse(BaseModel):
    id: int
    title: str
    message: str | None = None
    notification_type: str | None = None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
