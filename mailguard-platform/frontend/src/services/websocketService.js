const WS_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

// Hap lidhjen WebSocket per njoftimet live te perdoruesit
export function connectNotifications(userId, onNotification) {
  const socket = new WebSocket(`${WS_URL}/notifications?user_id=${userId}`);

  socket.onmessage = (event) => {
    onNotification(JSON.parse(event.data));
  };

  return socket;
}
