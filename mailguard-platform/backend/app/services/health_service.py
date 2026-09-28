from app.core.config import settings


# Ndertimi i pergjigjes se /health
def get_health_status():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "message": "Backend is running",
    }
