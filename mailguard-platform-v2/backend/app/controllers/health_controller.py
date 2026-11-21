from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Health"])


# GET /health - kontrolli me i thjeshte: a po punon backend-i
@router.get("/health")
def check_health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "message": "Backend is running",
    }
