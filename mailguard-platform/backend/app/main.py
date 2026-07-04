from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.controllers.health_controller import router as health_router
from app.controllers.auth_controller import router as auth_router

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

app.include_router(health_router)
app.include_router(auth_router)
