import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt, JWTError

from app.core.config import settings

JWT_ALGORITHM = "HS256"


# ---------- Fjalekalimet ----------

# Hash-on fjalekalimin me bcrypt (me salt te rastesishem)
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Krahason fjalekalimin e futur me hash-in e ruajtur ne databaze
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


# ---------- Access token (JWT, jetegjatesi e shkurter) ----------

# Krijon nje JWT qe mban id-ne e perdoruesit dhe kohen e skadimit
def create_access_token(user_id: int) -> str:
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expires_at}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=JWT_ALGORITHM)


# Kthen id-ne e perdoruesit nese tokeni eshte i vlefshem, perndryshe None
def read_user_id_from_access_token(access_token: str):
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        return None


# ---------- Refresh token (string i rastesishem, jetegjatesi e gjate) ----------

# Gjeneron nje string te gjate te rastesishem, te pamundur per t'u gjetur me hamendje
def create_refresh_token() -> str:
    return secrets.token_urlsafe(64)


# Ne databaze ruajme vetem hash-in e refresh tokenit, jo tokenin origjinal
def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode()).hexdigest()
