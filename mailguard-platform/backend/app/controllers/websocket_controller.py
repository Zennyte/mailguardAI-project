from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.websockets.connection_manager import manager

router = APIRouter(tags=["WebSocket"])


# WS /ws/notifications - lidhja live per njoftime
@router.websocket("/ws/notifications")
async def notifications_websocket(websocket: WebSocket, user_id: int):
    # Shenim: per thjeshtesi identifikohemi me user_id si query parameter.
    # Ne nje sistem real edhe ketu do te validohej JWT tokeni.
    await manager.connect(user_id, websocket)
    try:
        while True:
            # Mbajme lidhjen hapur; klienti nuk dergon asgje te rendesishme
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
