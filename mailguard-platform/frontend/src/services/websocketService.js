const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

// 
export function connectNotifications(userId, onNotification) {
  const socket = new WebSocket(`${WS_URL}/notifications?user_id=${userId}`);

  socket.onmessage = (event) => {
    onNotification(JSON.parse(event.data));
  };

  return socket;
}
