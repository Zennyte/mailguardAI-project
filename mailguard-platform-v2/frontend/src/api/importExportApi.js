// Kerkesat e faqes Import/Export (backend: import_export_controller.py)
import apiClient from "./apiClient";

// GET /data/export/{list_name} - merr skedarin nga backend-i dhe e shkarkon ne shfletues
export async function downloadExportedList(listName, fileFormat) {
  const response = await apiClient.get(`/data/export/${listName}`, {
    params: { file_format: fileFormat },
    responseType: "blob",
  });

  // Shkarkimi behet duke klikuar nje link te perkohshem qe tregon te skedari
  const fileUrl = URL.createObjectURL(response.data);
  const downloadLink = document.createElement("a");
  downloadLink.href = fileUrl;
  downloadLink.download = `${listName}.${fileFormat}`;
  downloadLink.click();
  URL.revokeObjectURL(fileUrl);
}

// POST /data/import/{list_name} - ngarkon skedarin; kthen sa rreshta u importuan
export async function importListFromFile(listName, file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await apiClient.post(`/data/import/${listName}`, formData);
  return response.data;
}
