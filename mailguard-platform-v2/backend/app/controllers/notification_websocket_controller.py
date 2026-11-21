# Lidhja live e kambanes se njoftimeve (WebSocket)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.core import security
from app.core.config import settings
from app.core.cookies import ACCESS_TOKEN_COOKIE
from app.websockets.notification_connections import notification_connections

router = APIRouter(tags=["WebSocket"])


# WS /ws/notifications
# Shfletuesi dergon vetem cookie-n "access_token" me lidhjen, prandaj nuk ka token ne URL.
@router.websocket("/ws/notifications")
async def notifications_websocket(websocket: WebSocket):
    # 1. Pranojme lidhje vetem nga faqja jone (mbron nga faqe te huaja qe hapin WebSocket)
    if websocket.headers.get("origin") != settings.FRONTEND_URL:
        await websocket.close(code=1008)
        return

    # 2. Perdoruesi duhet te jete i kycur
    access_token = websocket.cookies.get(ACCESS_TOKEN_COOKIE)
    user_id = security.read_user_id_from_access_token(access_token) if access_token else None
    if user_id is None:
        await websocket.close(code=1008)
        return

    await notification_connections.connect(user_id, websocket)
    try:
        while True:
            # Vetem e mbajme lidhjen hapur; klienti nuk dergon asgje te rendesishme
            await websocket.receive_text()
    except WebSocketDisconnect:
        notification_connections.disconnect(user_id, websocket)
