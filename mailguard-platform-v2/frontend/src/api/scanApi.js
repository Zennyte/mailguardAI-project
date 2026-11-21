// Kerkesat e faqeve Scanner, History dhe Dashboard (backend: scan_controller.py)
import apiClient from "./apiClient";

// POST /scans/analyze - skanon nje email dhe kthen rezultatin
export async function scanEmail(subject, body) {
  const response = await apiClient.post("/scans/analyze", { subject, body });
  return response.data;
}

// GET /scans - rreshtat e tabeles History
export async function getScanHistory() {
  const response = await apiClient.get("/scans");
  return response.data;
}

// GET /scans/stats - numrat e kartave ne Dashboard
export async function getScanStats() {
  const response = await apiClient.get("/scans/stats");
  return response.data;
}
