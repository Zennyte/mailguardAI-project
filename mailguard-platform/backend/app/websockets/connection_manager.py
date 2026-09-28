from fastapi import WebSocket


# Mban lidhjet WebSocket aktive per cdo perdorues dhe dergon njoftime live
class ConnectionManager:
    def __init__(self):
        # user_id -> lista e lidhjeve aktive (nje perdorues mund te kete disa tab-e)
        self.active_connections: dict = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: int, websocket: WebSocket):
        connections = self.active_connections.get(user_id, [])
        if websocket in connections:
            connections.remove(websocket)
        if not connections:
            self.active_connections.pop(user_id, None)

    async def send_to_user(self, user_id: int, message: dict):
        # Dergohet vetem nese perdoruesi eshte i lidhur ne ate moment
        for websocket in self.active_connections.get(user_id, []):
            await websocket.send_json(message)


manager = ConnectionManager()
