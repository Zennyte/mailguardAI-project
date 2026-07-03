from app.core.config import settings


def get_health_status():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "message": "Backend is running",
    }
