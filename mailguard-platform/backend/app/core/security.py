import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings

ALGORITHM = "HS256"


# Hash-on fjalekalimin me bcrypt (me salt te rastesishem)
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Krahason fjalekalimin e futur me hash-in e ruajtur
def verify_password(password: str, password_hash: str) -> bool:
    # Kontrollojme fjalekalimin e perdoruesit
    return bcrypt.checkpw(password.encode(), password_hash.encode())


# Krijon nje JWT access token (skadon pas 30 min)
def create_access_token(user_id: int) -> str:
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expires}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)


# Verifikon dhe deshifron nje access token, kthen user_id
def decode_access_token(token: str):
    # Kthen id-ne e perdoruesit nese tokeni eshte i vlefshem, perndryshe None
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None


# Gjeneron nje refresh token te rastesishem (jo JWT)
def create_refresh_token() -> str:
    # String i gjate i rastesishem, i pamundur per t'u gjetur me hamendje
    return secrets.token_urlsafe(64)


# Hash-on refresh tokenin (SHA-256) para se te ruhet ne DB
def hash_refresh_token(token: str) -> str:
    # Ne databaze ruajme vetem hash-in, jo tokenin origjinal
    return hashlib.sha256(token.encode()).hexdigest()
