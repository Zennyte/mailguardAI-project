import api from "./api";

// GET /notifications - njoftimet e perdoruesit
export async function getNotifications() {
  const response = await api.get("/notifications");
  return response.data;
}

// PATCH /notifications/{id}/read - shenon nje njoftim si te lexuar
export async function markAsRead(id) {
  const response = await api.patch(`/notifications/${id}/read`);
  return response.data;
}
