// Kerkesat e faqes Reports (backend: report_controller.py)
import apiClient from "./apiClient";

// GET /reports/preview - numrat e raportit pa e ruajtur
// "reportOptions" permban: report_type, date_from, date_to, label
export async function previewReport(reportOptions) {
  const response = await apiClient.get("/reports/preview", { params: reportOptions });
  return response.data;
}

// POST /reports - ruan raportin (emrin, llojin dhe filtrat)
export async function saveReport(reportName, reportOptions) {
  const response = await apiClient.post("/reports", { report_name: reportName, ...reportOptions });
  return response.data;
}

// GET /reports - lista "Saved reports"
export async function getSavedReports() {
  const response = await apiClient.get("/reports");
  return response.data;
}

// GET /reports/{id} - hap nje raport te ruajtur (numrat llogariten nga e para)
export async function openSavedReport(reportId) {
  const response = await apiClient.get(`/reports/${reportId}`);
  return response.data;
}
