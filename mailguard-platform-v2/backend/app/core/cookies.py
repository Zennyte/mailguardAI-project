from fastapi import Response

from app.core.config import settings

# Tokenat e kycjes ruhen ne dy cookie, jo ne localStorage te shfletuesit.
# Cookie me "httpOnly" nuk lexohet nga JavaScript, prandaj nje skript i huaj
# (sulm XSS) nuk mund t'i vjedhe tokenat.
ACCESS_TOKEN_COOKIE = "access_token"
REFRESH_TOKEN_COOKIE = "refresh_token"

# Refresh tokeni dergohet vetem te adresat /auth/... (refresh dhe logout),
# jo ne cdo kerkese - keshtu ekspozohet sa me pak.
REFRESH_TOKEN_COOKIE_PATH = "/auth"


# Vendos te dy cookie-t ne pergjigjen e login-it ose te refresh-it
def set_login_cookies(response: Response, access_token: str, refresh_token: str):
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE,
        value=access_token,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,                   # JavaScript nuk e lexon
        secure=settings.COOKIE_SECURE,   # vetem ne HTTPS (kur eshte True)
        samesite="lax",                  # nuk dergohet nga faqe te huaja (mbron nga CSRF)
        path="/",
    )
    response.set_cookie(
        key=REFRESH_TOKEN_COOKIE,
        value=refresh_token,
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite="lax",
        path=REFRESH_TOKEN_COOKIE_PATH,
    )


# Fshin te dy cookie-t (logout)
def clear_login_cookies(response: Response):
    response.delete_cookie(ACCESS_TOKEN_COOKIE, path="/")
    response.delete_cookie(REFRESH_TOKEN_COOKIE, path=REFRESH_TOKEN_COOKIE_PATH)
