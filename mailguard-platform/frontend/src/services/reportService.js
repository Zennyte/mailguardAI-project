import api from "./api";

// POST /reports - krijon dhe ruan nje raport te ri
export async function createReport(data) {
  const response = await api.post("/reports", data);
  return response.data;
}

// GET /reports - lista e raporteve te ruajtura
export async function getReports() {
  const response = await api.get("/reports");
  return response.data;
}

// GET /reports/{id} - hap nje raport (rigjenerohet live nga backend-i)
export async function getReport(id) {
  const response = await api.get(`/reports/${id}`);
  return response.data;
}

// GET /reports/preview - shikon nje raport pa e ruajtur
export async function previewReport(params) {
  const response = await api.get("/reports/preview", { params });
  return response.data;
}
