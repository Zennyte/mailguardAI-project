from fastapi import APIRouter

from app.services import health_service

router = APIRouter(tags=["Health"])


@router.get("/health")
def check_health():
    # Kontrolli me i thjeshte: a po punon backend-i
    return health_service.get_health_status()
