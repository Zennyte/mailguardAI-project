from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.controllers import (
    health_controller,
    auth_controller,
    scan_controller,
    notification_controller,
    notification_websocket_controller,
    search_controller,
    import_export_controller,
    report_controller,
    cms_controller,
)

app = FastAPI(
    title=settings.APP_NAME,
    description="Full-stack email scanning platform powered by Machine Learning",
)

# Lejojme kerkesat vetem nga frontend-i yne (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cdo controller mbulon nje pjese te faqes (shiko komentin ne krye te cdo skedari)
app.include_router(health_controller.router)
app.include_router(auth_controller.router)
app.include_router(scan_controller.router)
app.include_router(notification_controller.router)
app.include_router(notification_websocket_controller.router)
app.include_router(search_controller.router)
app.include_router(import_export_controller.router)
app.include_router(report_controller.router)
app.include_router(cms_controller.router)
