import api from "./api";

export async function exportData(entity, format) {
  const response = await api.get(`/data/export/${entity}`, {
    params: { format },
    responseType: "blob",
  });

  // Skedari shkarkohet direkt nga shfletuesi
  const url = URL.createObjectURL(response.data);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${entity}.${format}`;
  link.click();
  URL.revokeObjectURL(url);
}

export async function importData(entity, file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post(`/data/import/${entity}`, formData);
  return response.data;
}
