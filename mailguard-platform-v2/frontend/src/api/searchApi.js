// Kerkesa e faqes Search (backend: search_controller.py)
import apiClient from "./apiClient";

// GET /search?list_name=scans&search_text=...
// "filters" mund te permbaje: search_text, label, date_from, date_to, newest_first
export async function searchList(listName, filters) {
  const response = await apiClient.get("/search", {
    params: { list_name: listName, ...filters },
  });
  return response.data;
}
