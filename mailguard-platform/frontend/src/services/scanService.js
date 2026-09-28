import api from "./api";

// POST /scans/analyze - dergon emailin per skanim ML
export async function analyzeEmail(data) {
  const response = await api.post("/scans/analyze", data);
  return response.data;
}

// GET /scans - historiku i skanimeve
export async function getScanHistory() {
  const response = await api.get("/scans");
  return response.data;
}

// GET /scans/stats - statistikat per dashboard
export async function getScanStats() {
  const response = await api.get("/scans/stats");
  return response.data;
}
