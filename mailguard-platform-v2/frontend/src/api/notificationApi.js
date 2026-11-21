// Kerkesat e kambanes se njoftimeve (backend: notification_controller.py
// dhe notification_websocket_controller.py)
import apiClient from "./apiClient";

const WEBSOCKET_URL = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws";

// GET /notifications
export async function getNotifications() {
  const response = await apiClient.get("/notifications");
  return response.data;
}

// PATCH /notifications/{id}/read
export async function markNotificationAsRead(notificationId) {
  const response = await apiClient.patch(`/notifications/${notificationId}/read`);
  return response.data;
}

// Hap lidhjen live. Sa here qe backend-i dergon nje njoftim te ri,
// thirret onNewNotification(njoftimi). Kthen socket-in qe te mbyllet me vone.
// Shfletuesi e dergon vetem cookie-n e kycjes me lidhjen, prandaj nuk ka token ketu.
export function openNotificationSocket(onNewNotification) {
  const socket = new WebSocket(`${WEBSOCKET_URL}/notifications`);

  socket.onmessage = (event) => {
    onNewNotification(JSON.parse(event.data));
  };

  return socket;
}
