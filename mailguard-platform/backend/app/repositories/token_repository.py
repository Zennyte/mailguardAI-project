from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import RefreshToken


# Ruan hash-in e refresh tokenit ne DB
def save(db: Session, user_id: int, token_hash: str) -> RefreshToken:
    # Ne kolonen "token" ruhet hash-i i refresh tokenit
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_token)
    db.commit()
    return refresh_token


# Gjen nje refresh token te vlefshem (jo-revokuar, jo-skaduar)
def get_valid(db: Session, token_hash: str):
    # Vlen vetem nese nuk eshte revokuar dhe nuk ka skaduar
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token_hash,
            RefreshToken.is_revoked == False,  # noqa: E712
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )


# Revokon nje refresh token (s'perdoret me)
def revoke(db: Session, token_hash: str) -> bool:
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token_hash).first()
    if refresh_token is None:
        return False
    refresh_token.is_revoked = True
    db.commit()
    return True


# Revokon te gjitha refresh tokens e nje perdoruesi
def revoke_all_for_user(db: Session, user_id: int):
    db.query(RefreshToken).filter(RefreshToken.user_id == user_id).update({"is_revoked": True})
    db.commit()
