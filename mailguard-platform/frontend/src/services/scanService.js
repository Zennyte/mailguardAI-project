import api from "./api";

export async function analyzeEmail(data) {
  const response = await api.post("/scans/analyze", data);
  return response.data;
}

export async function getScanHistory() {
  const response = await api.get("/scans");
  return response.data;
}

export async function getScanStats() {
  const response = await api.get("/scans/stats");
  return response.data;
}
