from sqlalchemy.orm import Session

from app.models import AuditLog


# Regjistron nje veprim te perdoruesit (register / login / logout) ne audit_logs
def add_user_action(db: Session, user_id: int, action: str):
    db.add(AuditLog(user_id=user_id, action=action, entity="user", entity_id=user_id))
    db.commit()
