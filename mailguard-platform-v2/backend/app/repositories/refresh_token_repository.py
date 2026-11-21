from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models import RefreshToken

# Shenim: ne kolonen "token" ruhet hash-i i refresh tokenit, jo tokeni origjinal.
# Keshtu, nese dikush lexon databazen, nuk mund t'i perdore tokenat.


def save_refresh_token(db: Session, user_id: int, token_hash: str) -> RefreshToken:
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token_hash,
        expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )
    db.add(refresh_token)
    db.commit()
    return refresh_token


# Tokeni vlen vetem nese nuk eshte revokuar dhe nuk ka skaduar
def find_valid_refresh_token(db: Session, token_hash: str):
    return (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == token_hash,
            RefreshToken.is_revoked == False,  # noqa: E712
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
        .first()
    )


# Nje token i revokuar nuk mund te perdoret me.
# Kthen id-ne e perdoruesit te tokenit, ose None nese tokeni nuk ekziston.
def revoke_refresh_token(db: Session, token_hash: str):
    refresh_token = db.query(RefreshToken).filter(RefreshToken.token == token_hash).first()
    if refresh_token is None:
        return None
    refresh_token.is_revoked = True
    db.commit()
    return refresh_token.user_id
