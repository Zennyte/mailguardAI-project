from fastapi import WebSocket


# Mban lidhjet WebSocket te hapura te cdo perdoruesi, qe t'i dergojme njoftime live
class NotificationConnections:
    def __init__(self):
        # user_id -> lista e lidhjeve te hapura (nje perdorues mund te kete disa tab-e)
        self.connections_by_user_id: dict = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections_by_user_id.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        user_connections = self.connections_by_user_id.get(user_id, [])
        if websocket in user_connections:
            user_connections.remove(websocket)
        if not user_connections:
            self.connections_by_user_id.pop(user_id, None)

    # Dergohet vetem nese perdoruesi eshte i lidhur ne ate moment
    async def send_to_user(self, user_id: int, message: dict):
        for websocket in list(self.connections_by_user_id.get(user_id, [])):
            try:
                await websocket.send_json(message)
            except Exception:
                # Lidhja eshte mbyllur nderkohe - e heqim nga lista
                self.disconnect(user_id, websocket)


notification_connections = NotificationConnections()
