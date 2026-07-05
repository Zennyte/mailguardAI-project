import api from "./api";

export async function createReport(data) {
  const response = await api.post("/reports", data);
  return response.data;
}

export async function getReports() {
  const response = await api.get("/reports");
  return response.data;
}

export async function getReport(id) {
  const response = await api.get(`/reports/${id}`);
  return response.data;
}

export async function previewReport(params) {
  const response = await api.get("/reports/preview", { params });
  return response.data;
}
